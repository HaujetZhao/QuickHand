from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtSql import *
from PySide2.QtWidgets import *


class ConfigTab(QWidget):
    def __init__(self, parent, conn, preferenceTableName):
        super(ConfigTab, self).__init__(parent)
        self.conn = conn
        self.preferenceTableName = preferenceTableName
        self.initGui()
        self.connectSlots()
        self.initValues()

    def initGui(self):

        self.hideToSystemTraySwitch = QCheckBox(self.tr('点击关闭按钮时隐藏到托盘'))
        # self.chooseLanguageHint = QLabel(self.tr('语言：'))

        self.preferenceGroupLayout = QHBoxLayout()
        self.preferenceGroupLayout.addWidget(self.hideToSystemTraySwitch)
        self.preferenceGroup = QGroupBox(self.tr('偏好设置'))
        self.preferenceGroup.setLayout(self.preferenceGroupLayout)

        self.masterLayout = QVBoxLayout()
        self.masterLayout.addWidget(self.preferenceGroup)
        self.masterLayout.addStretch(1)

        self.setLayout(self.masterLayout)

    def initValues(self):
        self.checkDB()

    def connectSlots(self):
        self.hideToSystemTraySwitch.clicked.connect(self.hideToSystemTraySwitchClicked)

    def checkDB(self):
        cursor = self.conn.cursor()

        hideToSystemTrayResult = cursor.execute('''select value from %s where item = '%s'; ''' % (self.preferenceTableName, 'hideToTrayWhenHitCloseButton') ).fetchone()
        if hideToSystemTrayResult == None: # 如果关闭窗口最小化到状态栏这个选项还没有在数据库创建，那就创建一个
            cursor.execute('''insert into %s (item, value) values ('hideToTrayWhenHitCloseButton', 'False') ''' % self.preferenceTableName)
            self.conn.commit()
        else:
            hideToSystemTrayValue = hideToSystemTrayResult[0]
            if hideToSystemTrayValue == 'True':
                self.hideToSystemTraySwitch.setChecked(True)
            else:
                self.hideToSystemTraySwitch.setChecked(False)

    def hideToSystemTraySwitchClicked(self):
        cursor = self.conn.cursor()
        cursor.execute('''update %s set value='%s' where item = '%s';''' % (self.preferenceTableName, str(self.hideToSystemTraySwitch.isChecked()), 'hideToTrayWhenHitCloseButton'))
        self.conn.commit()
