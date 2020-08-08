# -*- coding: UTF-8 -*-

import os
import sys
import platform
import sqlite3

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtSql import *
from PySide2.QtWidgets import *

from moduels.SystemTray import SystemTray # 引入托盘栏
from moduels.HandRightTab import HandRightTab
from moduels.ConfigTab import ConfigTab
from moduels.HelpTab import HelpTab


dbname = './database.db'  # 存储预设的数据库名字
presetTableName = 'configPreset'  # 存储预设的表单名字
preferenceTableName = 'preference'
styleFile = './style.css'
version = 'V1.0.0'



############# 主窗口和托盘 ################

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initGui()
        self.loadStyleSheet()
        # self.status = self.statusBar() # 状态栏


        # self.setWindowState(Qt.WindowMaximized)
        # sys.stdout = Stream(newText=self.onUpdateText)

    def initGui(self):
        # 定义中心控件为多 tab 页面
        self.tabs = QTabWidget()
        QApplication.quit()
        self.setCentralWidget(self.tabs)

        # 定义多个不同功能的 tab
        self.handRightTab = HandRightTab(self, conn, presetTableName)  # 主要功能的 tab
        self.ConfigTab = ConfigTab(self, conn, preferenceTableName)  # 配置
        self.helpTab = HelpTab(version, platfm)  # 帮助

        self.tabs.addTab(self.handRightTab, self.tr('HandRight'))
        self.tabs.addTab(self.ConfigTab, self.tr('设置'))
        self.tabs.addTab(self.helpTab, self.tr('帮助'))
        self.adjustSize()

        # 设置图标
        if platfm == 'Windows':
            self.setWindowIcon(QIcon('icon.ico'))
        else:
            self.setWindowIcon(QIcon('icon.icns'))
        self.setWindowTitle('Quick Hand')

        # self.setWindowFlag(Qt.WindowStaysOnTopHint) # 始终在前台

        self.show()

    def loadStyleSheet(self):
        pass
        # global styleFile
        # try:
        #     try:
        #         with open(styleFile, 'r', encoding='utf-8') as style:
        #             self.setStyleSheet(style.read())
        #     except:
        #         with open(styleFile, 'r', encoding='gbk') as style:
        #             self.setStyleSheet(style.read())
        # except:
        #     QMessageBox.warning(self, self.tr('主题载入错误'), self.tr('未能成功载入主题，请确保软件根目录有 "style.css" 文件存在。'))

    def keyPressEvent(self, event) -> None:
        # 在按下 F5 的时候重载 style.css 主题
        if (event.key() == Qt.Key_F5):
            self.loadStyleSheet()

    def closeEvent(self, event):
        """Shuts down application on close."""
        # Return stdout to defaults.
        if main.ConfigTab.hideToSystemTraySwitch.isChecked():
            event.ignore()
            self.hide()
        else:
            sys.stdout = sys.__stdout__
            super().closeEvent(event)
        pass


def createDB():
    cursor = conn.cursor()
    result = cursor.execute('''select * from sqlite_master where name = '%s' ''' % presetTableName)
    if result.fetchone() == None:
        cursor.execute('''create table %s (
                                id integer primary key autoincrement,
                                name text,
                                useBackgroundImage integer,
                                imageName text,
                                backgroundSizeBoxX integer,
                                backgroundSizeBoxY integer,
                                fontName text,
                                fontSize integer,
                                fontColor text,
                                lineSpacing integer,
                                leftMargin integer,
                                topMargin integer,
                                rightMargin integer,
                                bottomMargin integer,
                                wordSpacing integer,
                                lineSpacingSigma integer,
                                fontSizeSigma integer,
                                wordSpacingSigma integer,
                                endChars text,
                                perturbXSigma integer,
                                perturbYSigma integer,
                                perturbThetaSigma real)''' % presetTableName)
        conn.commit()
    result = cursor.execute('''select * from sqlite_master where name = '%s' ''' % preferenceTableName)
    if result.fetchone() == None:
        cursor.execute('''create table %s (
                                id integer primary key autoincrement,
                                item text,
                                value text
                                )''' % preferenceTableName)
        conn.commit()
        print(1)

if __name__ == '__main__':
    os.environ['PATH'] += os.pathsep + os.getcwd()
    app = QApplication(sys.argv)
    conn = sqlite3.connect(dbname)
    createDB()
    platfm = platform.system()
    main = MainWindow()
    if platfm == 'Windows':
        tray = SystemTray(QIcon('icon.ico'), main)
    else:
        tray = SystemTray(QIcon('icon.icns'), main)
    sys.exit(app.exec_())
    conn.close()
