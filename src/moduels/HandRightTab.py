import os
import sqlite3

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from PIL import Image, ImageFont
from handright import Template, handwrite

from moduels.GenerateImagesThread import GenerateImagesThread
from moduels.ConsoleWindow import ConsoleWindow
from moduels.ColorLabel import ColorLabel
# 参考 https://github.com/Gsllchb/Handright/blob/master/docs/tutorial.md

class HandRightTab(QWidget):
    def __init__(self, parent, conn, presetTableName):
        super(HandRightTab, self).__init__(parent)
        self.conn = conn
        self.presetTableName = presetTableName
        self.initGui()
        self.refreshList()
        self.connectSlots()
        self.initValue()

    def initGui(self):

        self.inputBox = QPlainTextEdit()

        self.outputPathHint = QLabel('输出路径')
        self.outputPathBox = QLineEdit()

        self.runBtn = QPushButton('运行')

        self.backgroundBlankRadioBtn = QRadioButton('使用空白背景')
        self.backgroundImageRadioBtn = QRadioButton('使用背景图片')


        self.backgroundHint = QLabel('背景图片')
        self.backgroundBox = QComboBox()

        self.backgroundSizeHint = QLabel('背景图片大小')
        self.backgroundSizeBoxX = QLineEdit()
        self.backgroundSizeBoxMultipleHint = QLabel('×')
        self.backgroundSizeBoxY = QLineEdit()


        self.fontPathHint = QLabel('字体')
        self.fontPathBox = QComboBox()

        self.fontSizeHint = QLabel('字体大小')
        self.fontSizeBox = QSpinBox()

        self.fontColorHint = QLabel('字体颜色')
        self.fontColorBox = ColorLabel('')

        self.lineSpacingHint = QLabel('行间距')
        self.lineSpacingBox = QSpinBox()

        self.wordSpacingHint = QLabel('字符间距')
        self.wordSpacingBox = QSpinBox()



        self.leftMarginHint = QLabel('页面左边距')
        self.leftMarginBox = QSpinBox()

        self.topMarginHint = QLabel('页面上边距')
        self.topMarginBox = QSpinBox()

        self.rightMarginHint = QLabel('页面右边距')
        self.rightMarginBox = QSpinBox()

        self.bottomMarginHint = QLabel('页面下边距')
        self.bottomMarginBox = QSpinBox()



        self.lindSpacingSigmaHint = QLabel('行间距扰动')
        self.lindSpacingSigmaBox = QSpinBox()

        self.fontSizeSigmaHint = QLabel('字体大小扰动')
        self.fontSizeSigmaBox = QSpinBox()

        self.wordSpacingSigmaHint = QLabel('字间距扰动')
        self.wordSpacingSigmaBox = QSpinBox()

        self.perturbXSigmaHint = QLabel('笔画横向偏移扰动')
        self.perturbXSigmaBox = QSpinBox()

        self.perturbYSigmaHint = QLabel('笔画纵向偏移扰动')
        self.perturbYSigmaBox = QSpinBox()

        self.perturbThetaSigmaHint = QLabel('笔画旋转偏移扰动')
        self.perturbThetaSigmaBox = QDoubleSpinBox()

        self.endCharsHint = QLabel('防止行首字符')
        self.endCharsBox = QLineEdit()

        self.showImageBox = QCheckBox('每生成一张图片后自动打开')

        self.presetHint = QLabel('预设列表')
        self.presetList = QListWidget()

        self.upPresetBtn = QPushButton('↑')
        self.downPresetBtn = QPushButton('↓')
        self.addPresetBtn = QPushButton('+')
        self.delPresetBtn = QPushButton('-')


        self.outputLayout = QHBoxLayout()
        self.outputLayout.setContentsMargins(0,0,0,0)
        self.outputLayout.addWidget(self.outputPathHint)
        self.outputLayout.addWidget(self.outputPathBox)
        self.outputBox = QWidget()
        self.outputBox.setContentsMargins(0,0,0,0)
        self.outputBox.setLayout(self.outputLayout)
        self.inputAndRunLayout = QVBoxLayout()
        self.inputAndRunLayout.addWidget(self.inputBox)
        self.inputAndRunLayout.addWidget(self.outputBox)
        self.inputAndRunLayout.addWidget(self.runBtn)
        self.inputAndRunBox = QWidget()
        self.inputAndRunBox.setLayout(self.inputAndRunLayout)




        self.backgroundTypeLayout = QHBoxLayout()  # 关于背景类型的两个按钮放置的布局
        self.backgroundTypeLayout.addWidget(self.backgroundBlankRadioBtn)
        self.backgroundTypeLayout.addWidget(self.backgroundImageRadioBtn)
        self.backgroundTypeBox = QWidget()
        self.backgroundTypeBox.setContentsMargins(0,0,0,0)
        self.backgroundTypeBox.setLayout(self.backgroundTypeLayout)

        self.backgroundSizeLayout = QHBoxLayout()  # 关于背景大小
        self.backgroundSizeLayout.setContentsMargins(0,0,0,0)
        self.backgroundSizeLayout.addWidget(self.backgroundSizeBoxX)
        self.backgroundSizeLayout.addWidget(self.backgroundSizeBoxMultipleHint)
        self.backgroundSizeLayout.addWidget(self.backgroundSizeBoxY)
        self.backgroundSizeBox = QWidget()
        self.backgroundSizeBox.setContentsMargins(0, 0, 0, 0)
        self.backgroundSizeBox.setLayout(self.backgroundSizeLayout)

        self.optionsLayout = QFormLayout()
        self.optionsLayout.setWidget(0, QFormLayout.SpanningRole, self.backgroundTypeBox) # 背景类型
        self.optionsLayout.addRow(self.backgroundHint, self.backgroundBox)  # 背景图片
        self.optionsLayout.setWidget(2, QFormLayout.LabelRole, self.backgroundSizeHint) # 背景大小
        self.optionsLayout.setWidget(2, QFormLayout.FieldRole, self.backgroundSizeBox) # 背景大小
        self.optionsLayout.addRow(QLabel(''), QLabel(''))  # 空白行
        self.optionsLayout.addRow(self.fontPathHint, self.fontPathBox)  # 字体
        self.optionsLayout.addRow(self.fontSizeHint, self.fontSizeBox)  # 字体大小
        self.optionsLayout.addRow(self.fontColorHint, self.fontColorBox)  # 字体颜色
        self.optionsLayout.addRow(self.lineSpacingHint, self.lineSpacingBox)  # 行间距
        self.optionsLayout.addRow(self.wordSpacingHint, self.wordSpacingBox)  # 字符间距
        self.optionsLayout.addRow(QLabel(''), QLabel(''))  # 空白行
        self.optionsLayout.addRow(self.leftMarginHint, self.leftMarginBox)  # 左边距
        self.optionsLayout.addRow(self.topMarginHint, self.topMarginBox)  # 上边距
        self.optionsLayout.addRow(self.rightMarginHint, self.rightMarginBox)  # 右边距
        self.optionsLayout.addRow(self.bottomMarginHint, self.bottomMarginBox)  # 下边距
        self.optionsLayout.addRow(QLabel(''), QLabel(''))  # 空白行
        self.optionsLayout.addRow(self.lindSpacingSigmaHint, self.lindSpacingSigmaBox)  # 行间距扰动
        self.optionsLayout.addRow(self.fontSizeSigmaHint, self.fontSizeSigmaBox)  # 字体大小扰动
        self.optionsLayout.addRow(self.wordSpacingSigmaHint, self.wordSpacingSigmaBox)  # 字间距扰动
        self.optionsLayout.addRow(self.perturbXSigmaHint, self.perturbXSigmaBox)  # 笔画横向偏移扰动
        self.optionsLayout.addRow(self.perturbYSigmaHint, self.perturbYSigmaBox)  # 行间距扰动
        self.optionsLayout.addRow(self.perturbThetaSigmaHint, self.perturbThetaSigmaBox)  # 行间距扰动
        self.optionsLayout.addRow(self.endCharsHint, self.endCharsBox)  # 防止行首字符
        self.optionsLayout.addRow(QLabel(''), QLabel(''))  # 空白行
        self.optionsLayout.setWidget(23, QFormLayout.SpanningRole, self.showImageBox)


        self.optionsBox = QWidget()
        self.optionsBox.setLayout(self.optionsLayout)


        self.presetLayout = QGridLayout()
        self.presetLayout.addWidget(self.presetHint, 0,0,1,2)
        self.presetLayout.addWidget(self.presetList, 1,0,1,2)
        self.presetLayout.addWidget(self.upPresetBtn, 2,0,1,1)
        self.presetLayout.addWidget(self.downPresetBtn, 2,1,1,1)
        self.presetLayout.addWidget(self.addPresetBtn, 3,0,1,1)
        self.presetLayout.addWidget(self.delPresetBtn, 3,1,1,1)
        self.presetBox = QWidget()
        self.presetBox.setLayout(self.presetLayout)



        self.splitBetweenOptionAndPesetTable = QSplitter()
        self.splitBetweenOptionAndPesetTable.addWidget(self.optionsBox)
        self.splitBetweenOptionAndPesetTable.addWidget(self.presetBox)

        self.splitBetweenInputAndOption = QSplitter()
        self.splitBetweenInputAndOption.addWidget(self.inputAndRunBox)
        self.splitBetweenInputAndOption.addWidget(self.splitBetweenOptionAndPesetTable)

        self.masterLayout = QHBoxLayout()
        self.masterLayout.addWidget(self.splitBetweenInputAndOption)

        self.setLayout(self.masterLayout)

    def initValue(self):
        font = QFont()
        font.setPointSize(12)
        self.inputBox.setFont(font)
        self.inputBox.setPlaceholderText('在这里输入要生成图片的文字')

        self.outputPathBox.setText(os.getcwd().replace('\\', '/') + '/output')

        self.backgroundBlankRadioBtn.click() # 启用或停用背景图片
        # self.switchUseable()

        self.backgroundBox.clear()
        self.backgroundBox.addItems(os.listdir('./backgrounds')) # 添加背景图片列表

        self.backgroundSizeBoxX.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter) # 初始化背景图片大小
        self.backgroundSizeBoxX.setValidator(QIntValidator(self))
        self.backgroundSizeBoxX.setText('2000')

        self.backgroundSizeBoxY.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter) # 初始化背景图片大小
        self.backgroundSizeBoxY.setValidator(QIntValidator(self))
        self.backgroundSizeBoxY.setText('2000')


        self.fontPathBox.clear()
        self.fontPathBox.addItems(os.listdir('./fonts')) # 添加字体列表

        self.fontSizeBox.setSingleStep(5)
        self.fontSizeBox.setMinimum(1)
        self.fontSizeBox.setMaximum(2000)
        self.fontSizeBox.setValue(100)  # 设定字体初始大小
        self.fontSizeBox.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.lineSpacingBox.setSingleStep(10)
        self.lineSpacingBox.setMinimum(1)
        self.lineSpacingBox.setMaximum(2000)
        self.lineSpacingBox.setValue(120)  # 初始化行间距
        self.lineSpacingBox.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.wordSpacingBox.setSingleStep(5)
        self.wordSpacingBox.setMinimum(-1000)
        self.wordSpacingBox.setMaximum(2000)
        self.wordSpacingBox.setValue(120)  # 初始化字符间距
        self.wordSpacingBox.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.leftMarginBox.setSingleStep(5)
        self.leftMarginBox.setMinimum(1)
        self.leftMarginBox.setMaximum(2000)
        self.leftMarginBox.setValue(200)  # 初始化页面左边距
        self.leftMarginBox.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.topMarginBox.setSingleStep(5)
        self.topMarginBox.setMinimum(1)
        self.topMarginBox.setMaximum(2000)
        self.topMarginBox.setValue(200)  # 初始化页面上边距
        self.topMarginBox.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.rightMarginBox.setSingleStep(5)
        self.rightMarginBox.setMinimum(1)
        self.rightMarginBox.setMaximum(2000)
        self.rightMarginBox.setValue(200)  # 初始化页面右边剧
        self.rightMarginBox.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.bottomMarginBox.setSingleStep(5)
        self.bottomMarginBox.setMinimum(1)
        self.bottomMarginBox.setMaximum(2000)
        self.bottomMarginBox.setValue(200)  # 初始化页面下边距
        self.bottomMarginBox.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.lindSpacingSigmaBox.setSingleStep(1)
        self.lindSpacingSigmaBox.setMinimum(1)
        self.lindSpacingSigmaBox.setMaximum(1000)
        self.lindSpacingSigmaBox.setValue(6)  # 初始化行间距扰动
        self.lindSpacingSigmaBox.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.fontSizeSigmaBox.setSingleStep(2)
        self.fontSizeSigmaBox.setMinimum(1)
        self.fontSizeSigmaBox.setMaximum(1000)
        self.fontSizeSigmaBox.setValue(20)  # 初始化字体大小扰动
        self.fontSizeSigmaBox.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.wordSpacingSigmaBox.setSingleStep(1)
        self.wordSpacingSigmaBox.setMinimum(1)
        self.wordSpacingSigmaBox.setMaximum(1000)
        self.wordSpacingSigmaBox.setValue(3)  # 初始化字间距扰动
        self.wordSpacingSigmaBox.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.perturbXSigmaBox.setSingleStep(1)
        self.perturbXSigmaBox.setMinimum(1)
        self.perturbXSigmaBox.setMaximum(1000)
        self.perturbXSigmaBox.setValue(4)  # 笔画横向偏移扰动
        self.perturbXSigmaBox.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.perturbYSigmaBox.setSingleStep(1)
        self.perturbYSigmaBox.setMinimum(1)
        self.perturbYSigmaBox.setMaximum(1000)
        self.perturbYSigmaBox.setValue(4)  # 笔画纵向偏移扰动
        self.perturbYSigmaBox.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.perturbThetaSigmaBox.setSingleStep(1)
        self.perturbThetaSigmaBox.setDecimals(2)
        self.perturbThetaSigmaBox.setMinimum(0.00)
        self.perturbThetaSigmaBox.setMaximum(1)
        self.perturbThetaSigmaBox.setValue(0.05)  # 笔画旋转偏移扰动
        self.perturbThetaSigmaBox.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.endCharsBox.setText('，。！？')  # 防止行首字符
        self.endCharsBox.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)


        self.splitBetweenInputAndOption.setStretchFactor(0,5)
        self.splitBetweenInputAndOption.setStretchFactor(1,1)


    def connectSlots(self):
        self.runBtn.clicked.connect(self.run)
        self.backgroundBlankRadioBtn.clicked.connect(self.backgroundBlankRadioBtnClicked)
        self.backgroundImageRadioBtn.clicked.connect(self.backgroundImageRadioBtnClicked)
        self.upPresetBtn.clicked.connect(self.upMovePreset)
        self.downPresetBtn.clicked.connect(self.downMovePreset)
        self.addPresetBtn.clicked.connect(self.addPreset)
        self.delPresetBtn.clicked.connect(self.delPreset)
        self.presetList.itemClicked.connect(self.presetItemSelected)


    def backgroundBlankRadioBtnClicked(self):
        self.useBackgroundImage = False
        self.backgroundHint.setEnabled(False)
        self.backgroundBox.setEnabled(False)
        self.backgroundSizeHint.setText('背景图片大小')
        self.backgroundSizeBoxX.setText('2000')
        self.backgroundSizeBoxY.setText('4000')

    def backgroundImageRadioBtnClicked(self):
        self.useBackgroundImage = True
        self.backgroundHint.setEnabled(True)
        self.backgroundBox.setEnabled(True)
        self.backgroundSizeHint.setText('背景图片缩放')
        self.backgroundSizeBoxX.setText('1')
        self.backgroundSizeBoxY.setText('1')

    def refreshList(self):
        cursor = self.conn.cursor()
        try:
            result = cursor.execute('''select name from %s order by id asc''' % (self.presetTableName)).fetchall()
        except:
            print('数据库读取不正常') # 这里可能还需要加一个重新载入数据库的操作, 不过懒得写了
        self.presetList.clear()
        for item in result:
            self.presetList.addItem(item[0])

    def presetItemSelected(self):
        currentRow = self.presetList.currentRow()
        currentItemName = self.presetList.item(currentRow).text()
        presetData = self.conn.cursor().execute('''select 
                                                        useBackgroundImage, imageName, 
                                                        backgroundSizeBoxX, backgroundSizeBoxY, fontName, fontSize, 
                                                        fontColor, lineSpacing, leftMargin, topMargin, 
                                                        rightMargin, bottomMargin, wordSpacing, lineSpacingSigma, 
                                                        fontSizeSigma, wordSpacingSigma, endChars, perturbXSigma, 
                                                        perturbYSigma, perturbThetaSigma
                                                    from %s where name = '%s'; ''' % (
                                                        self.presetTableName, currentItemName)).fetchone()

        useBackgroundImage = presetData[0]
        imageName = presetData[1]
        backgroundSizeBoxX = presetData[2]
        backgroundSizeBoxY = presetData[3]
        fontName = presetData[4]
        fontSize = presetData[5]
        fontColor = presetData[6]
        lineSpacing = presetData[7]
        leftMargin = presetData[8]
        topMargin = presetData[9]
        rightMargin = presetData[10]
        bottomMargin = presetData[11]
        wordSpacing = presetData[12]
        lineSpacingSigma = presetData[13]
        fontSizeSigma = presetData[14]
        wordSpacingSigma = presetData[15]
        endChars = presetData[16]
        perturbXSigma = presetData[17]
        perturbYSigma = presetData[18]
        perturbThetaSigma = presetData[19]

        if useBackgroundImage:
            self.backgroundImageRadioBtn.click()
        else:
            self.backgroundBlankRadioBtn.click()
        self.backgroundBox.setCurrentText(imageName)
        self.backgroundSizeBoxX.setText(str(backgroundSizeBoxX))
        self.backgroundSizeBoxY.setText(str(backgroundSizeBoxY))
        self.fontPathBox.setCurrentText(fontName)
        self.fontSizeBox.setValue(fontSize)
        colorTuple = tuple(eval(fontColor))
        print(colorTuple)
        self.fontColorBox.color = QColor()
        self.fontColorBox.color.setRgb(colorTuple[0], colorTuple[1], colorTuple[2])
        self.fontColorBox.setColor()
        self.lineSpacingBox.setValue(lineSpacing)
        self.leftMarginBox.setValue(leftMargin)
        self.topMarginBox.setValue(topMargin)
        self.rightMarginBox.setValue(rightMargin)
        self.bottomMarginBox.setValue(bottomMargin)
        self.wordSpacingBox.setValue(wordSpacing)
        self.lindSpacingSigmaBox.setValue(lineSpacingSigma)
        self.fontSizeSigmaBox.setValue(fontSizeSigma)
        self.wordSpacingSigmaBox.setValue(wordSpacingSigma)
        self.endCharsBox.setText(endChars)
        self.perturbXSigmaBox.setValue(perturbXSigma)
        self.perturbYSigmaBox.setValue(perturbYSigma)
        self.perturbThetaSigmaBox.setValue(perturbThetaSigma)


    def addPreset(self):
        presetName, _ = QInputDialog.getText(self,'添加或更新预设','请输入预设名称')

        print(presetName)
        if _ == False:
            return False
        imageName = self.backgroundBox.currentText().replace("'", "''")
        imageSizeX = int(self.backgroundSizeBoxX.text())
        imageSizeY = int(self.backgroundSizeBoxY.text())
        fontName = self.fontPathBox.currentText().replace("'", "''")
        fontSize = self.fontSizeBox.value()
        fontColor = self.fontColorBox.color
        fontColor = (fontColor.red(), fontColor.green(), fontColor.blue())
        lineSpacing = self.lineSpacingBox.value()
        leftMargin = self.leftMarginBox.value()
        topMargin = self.topMarginBox.value()
        rightMargin = self.rightMarginBox.value()
        bottomMargin = self.bottomMarginBox.value()
        wordSpacing = self.wordSpacingBox.value()
        lineSpacingSigma = self.lindSpacingSigmaBox.value()
        fontSizeSigma = self.fontSizeSigmaBox.value()
        wordSpacingSigma = self.wordSpacingSigmaBox.value()
        endChars = self.endCharsBox.text().replace("'", "''")
        perturbXSigma = self.perturbXSigmaBox.value()
        perturbYSigma = self.perturbYSigmaBox.value()
        perturbThetaSigma = self.perturbThetaSigmaBox.value()

        cursor = self.conn.cursor()
        result = cursor.execute('''select name from %s where name = '%s';''' % (self.presetTableName, presetName.replace("'", "''"))).fetchone()
        if result == None: # 如果没有重名的预设
            maxIdItem = cursor.execute('''select id from %s order by id desc;''' % (self.presetTableName)).fetchone()
            if maxIdItem == None:
                maxId = 0
            else:
                maxId = maxIdItem[0]
            print(maxId)
            cursor.execute('''insert into %s (id, name, useBackgroundImage, imageName, 
                                            backgroundSizeBoxX, backgroundSizeBoxY, fontName, fontSize, 
                                            fontColor, lineSpacing, leftMargin, topMargin, 
                                            rightMargin, bottomMargin, wordSpacing, lineSpacingSigma, 
                                            fontSizeSigma, wordSpacingSigma, endChars, perturbXSigma, 
                                            perturbYSigma, perturbThetaSigma) 
                                    values (%s, '%s', %s, '%s', 
                                            %s, %s, '%s', %s, 
                                            '%s', %s, %s, %s, 
                                            %s, %s, %s, %s, 
                                            %s, %s, '%s', %s, 
                                            %s, %s);'''
                   % (self.presetTableName, maxId+1, presetName, self.useBackgroundImage, imageName,
                                            imageSizeX, imageSizeY, fontName, fontSize,
                                            fontColor, lineSpacing, leftMargin, topMargin,
                                            rightMargin, bottomMargin, wordSpacing, lineSpacingSigma,
                                            fontSizeSigma, wordSpacingSigma, endChars, perturbXSigma,
                                            perturbYSigma, perturbThetaSigma))
        else: # 如果有重名的预设
            answer = QMessageBox.question(self, '更新预设', '已经存在相同名字的预设，是否更新？', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if answer != QMessageBox.Yes:
                return False
            print(answer)
            cursor.execute('''update %s set useBackgroundImage=%s, imageName='%s', 
                                            backgroundSizeBoxX=%s, backgroundSizeBoxY=%s, fontName='%s', fontSize=%s, 
                                            fontColor='%s', lineSpacing=%s, leftMargin=%s, topMargin=%s, 
                                            rightMargin=%s, bottomMargin=%s, wordSpacing=%s, lineSpacingSigma=%s, 
                                            fontSizeSigma=%s, wordSpacingSigma=%s, endChars='%s', perturbXSigma=%s, 
                                            perturbYSigma=%s, perturbThetaSigma=%s where name = '%s' '''
                    % (self.presetTableName, self.useBackgroundImage, imageName,
                                            imageSizeX, imageSizeY, fontName, fontSize,
                                            fontColor, lineSpacing, leftMargin, topMargin,
                                            rightMargin, bottomMargin, wordSpacing, lineSpacingSigma,
                                            fontSizeSigma, wordSpacingSigma, endChars, perturbXSigma,
                                            perturbYSigma, perturbThetaSigma, presetName))
            QMessageBox.information(self, '成功', '预设更新成功')
        self.conn.commit()
        self.refreshList()

    def delPreset(self):
        currentRow = self.presetList.currentRow()
        if currentRow < 0:
            return False
        currentItemName = self.presetList.item(currentRow).text()
        answer = QMessageBox.question(self, '删除预设', '确认要删除“%s”预设吗？' % currentItemName)
        if answer == QMessageBox.No:
            return False
        id = self.conn.cursor().execute('''select id from %s where name = '%s'; ''' % (self.presetTableName, currentItemName)).fetchone()[0]
        self.conn.cursor().execute("delete from %s where id = '%s'; " % (self.presetTableName, id))
        self.conn.cursor().execute("update %s set id=id-1 where id > %s" % (self.presetTableName, id))
        self.conn.commit()
        self.refreshList()

    def upMovePreset(self):
        currentRow = self.presetList.currentRow()
        if currentRow < 1:
            return False
        currentItemName = self.presetList.currentItem().text().replace("'", "''")
        id = self.conn.cursor().execute(
            "select id from %s where name = '%s'" % (self.presetTableName, currentItemName)).fetchone()[0]
        self.conn.cursor().execute("update %s set id=10000 where id=%s-1 " % (self.presetTableName, id))
        self.conn.cursor().execute("update %s set id = id - 1 where name = '%s'" % (self.presetTableName, currentItemName))
        self.conn.cursor().execute("update %s set id=%s where id=10000 " % (self.presetTableName, id))
        self.conn.commit()
        self.refreshList()
        self.presetList.setCurrentRow(currentRow - 1)

    def downMovePreset(self):
        currentRow = self.presetList.currentRow()
        totalRow = self.presetList.count()
        if currentRow < 0 or currentRow > totalRow - 2:
            return False
        currentItemName = self.presetList.currentItem().text().replace("'", "''")
        id = self.conn.cursor().execute(
            "select id from %s where name = '%s'" % (self.presetTableName, currentItemName)).fetchone()[0]
        self.conn.cursor().execute("update %s set id=10000 where id=%s+1 " % (self.presetTableName, id))
        self.conn.cursor().execute("update %s set id = id + 1 where name = '%s'" % (self.presetTableName, currentItemName))
        self.conn.cursor().execute("update %s set id=%s where id=10000 " % (self.presetTableName, id))
        self.conn.commit()
        self.refreshList()
        if currentRow < totalRow:
            self.presetList.setCurrentRow(currentRow + 1)
        else:
            self.presetList.setCurrentRow(currentRow)

    def run(self):
        if not self.checkOutputPath(): # 如果输出检查发生了错误 就停止
            return False
        if self.fontPathBox.currentText() == '':
            QMessageBox.information(self, '字体问题', '选择的字体为空，运行停止。请将 ttf 格式的字体放到本软件根目录的 fonts 文件夹中，再重新启动软件。')
            return False
        if self.useBackgroundImage:
            imageName = self.backgroundBox.currentText()  # 图片文件名
            if imageName == '':
                QMessageBox.warning(self, '背景问题', '你选择了使用图片背景，但背景图片文件为空，运行停止。请将 jpg、png 格式的图片放到本软件根目录的 backgrounds 文件夹中，再重新启动软件。')
                return False
        if (self.backgroundSizeBoxX.text() == '' or self.backgroundSizeBoxY.text() == '') or (int(self.backgroundSizeBoxX.text()) == 0 or int(self.backgroundSizeBoxY.text()) == 0):
            QMessageBox.warning(self, '背景问题', '背景图片大小错误，请检查')
            return False
        inputText = self.inputBox.toPlainText()
        if inputText == '':
            print('没有输入文字')
            return False

        # 背景图片
        imageSizeX = int(self.backgroundSizeBoxX.text())
        imageSizeY = int(self.backgroundSizeBoxY.text())
        if not self.useBackgroundImage:
            background = Image.new(mode="RGB", size=(imageSizeX, imageSizeY),color=(255, 255, 255))
        else:
            imagePath = os.path.abspath('./backgrounds/' + imageName)
            try:
                background = Image.open(imagePath, 'r')
            except:
                QMessageBox.warning(self, '背景问题', '所选背景图片不是可打开的图片文件')
                return False
            width, height = background.size
            background = background.resize((width * imageSizeX, height * imageSizeY), resample=Image.LANCZOS)

        # 字体文件
        fontName = self.fontPathBox.currentText()
        fontPath = os.path.abspath('./fonts/' + fontName)
        try:
            font = ImageFont.truetype(fontPath)
        except:
            QMessageBox.warning(self, '字体问题', '所选字体不是可打开的 ttf 字体文件')
            return False

        fontSize = self.fontSizeBox.value()
        fontColor = self.fontColorBox.color
        fontColor = (fontColor.red(), fontColor.green(), fontColor.blue())
        lineSpacing = self.lineSpacingBox.value()
        leftMargin = self.leftMarginBox.value()
        topMargin = self.topMarginBox.value()
        rightMargin = self.rightMarginBox.value()
        bottomMargin = self.bottomMarginBox.value()
        wordSpacing = self.wordSpacingBox.value()
        lineSpacingSigma = self.lindSpacingSigmaBox.value()
        fontSizeSigma = self.fontSizeSigmaBox.value()
        wordSpacingSigma = self.wordSpacingSigmaBox.value()
        endChars = self.endCharsBox.text()
        perturbXSigma = self.perturbXSigmaBox.value()
        perturbYSigma = self.perturbYSigmaBox.value()
        perturbThetaSigma = self.perturbThetaSigmaBox.value()
        showImage = self.showImageBox.isChecked()


        template = Template(
            background=background,
            font_size=fontSize,
            font=font,
            line_spacing=lineSpacing,
            fill=fontColor,  # 字体“颜色”
            left_margin=leftMargin,
            top_margin=topMargin,
            right_margin=rightMargin,
            bottom_margin=bottomMargin,
            word_spacing=wordSpacing,
            line_spacing_sigma=lineSpacingSigma,  # 行间距随机扰动
            font_size_sigma=fontSizeSigma,  # 字体大小随机扰动
            word_spacing_sigma=wordSpacingSigma,  # 字间距随机扰动
            end_chars=endChars,  # 防止特定字符因排版算法的自动换行而出现在行首
            perturb_x_sigma=perturbXSigma,  # 笔画横向偏移随机扰动
            perturb_y_sigma=perturbYSigma,  # 笔画纵向偏移随机扰动
            perturb_theta_sigma=perturbThetaSigma,  # 笔画旋转偏移随机扰动
        )

        window = ConsoleWindow(self.parent())
        thread = GenerateImagesThread()
        window.thread = thread
        thread.text = inputText
        thread.template = template
        thread.outputPath = self.outputPath
        thread.showImage = showImage
        thread.signal.connect(window.consolePrintBox.print)
        thread.start()




    def checkOutputPath(self):
        self.outputPath = self.outputPathBox.text()
        if not os.path.exists(self.outputPath): # 如果输出路径不存在
            respond = QMessageBox.question(self, '路径错误', '输出文件夹不存在，是否创建？', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if respond == QMessageBox.Yes:
                try:
                    os.mkdir(self.outputPath)
                    return True
                except:
                    QMessageBox.warning(self, '路径错误', '无法创建输出文件夹，请检查输出路径')
                    return False
            else:
                return False # 任务取消
        else:
            return True # 路径存在, 继续任务



    # 启用和停用某些选项
    def switchUseable(self):
        if self.backgroundSwitch.isChecked() == False:
            self.backgroundHint.setEnabled(False)
            self.backgroundBox.setEnabled(False)
        else:
            self.backgroundHint.setEnabled(True)
            self.backgroundBox.setEnabled(True)








