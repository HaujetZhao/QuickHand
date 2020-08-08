import webbrowser
import os

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtSql import *
from PySide2.QtWidgets import *

from moduels.SponsorDialog import SponsorDialog


# 帮助页面
class HelpTab(QWidget):
    def __init__(self, version, platfm):
        super().__init__()
        self.platfm = platfm
        self.openHelpFileButton = QPushButton(self.tr('打开帮助文档'))
        self.openVideoHelpButtone = QPushButton(self.tr('查看视频教程'))
        self.openGiteePage = QPushButton(self.tr('当前版本是 %s，到 Gitee 检查新版本') % version)
        self.openGithubPage = QPushButton(self.tr('当前版本是 %s，到 Github 检查新版本') % version)
        self.linkToDiscussPage = QPushButton(self.tr('加入 QQ 群'))
        self.tipButton = QPushButton(self.tr('打赏作者'))

        self.openHelpFileButton.setMaximumHeight(100)
        self.openVideoHelpButtone.setMaximumHeight(100)
        self.openGiteePage.setMaximumHeight(100)
        self.openGithubPage.setMaximumHeight(100)
        self.linkToDiscussPage.setMaximumHeight(100)
        self.tipButton.setMaximumHeight(100)

        self.openHelpFileButton.clicked.connect(self.openHelpDocument)
        self.openVideoHelpButtone.clicked.connect(lambda: webbrowser.open(self.tr(r'https://www.bilibili.com/video/BV14a4y1J7X8/')))
        self.openGiteePage.clicked.connect(lambda: webbrowser.open(self.tr(r'https://gitee.com/haujet/QuickHand/releases')))
        self.openGithubPage.clicked.connect(lambda: webbrowser.open(self.tr(r'https://github.com/HaujetZhao/QuickHand/releases')))
        self.linkToDiscussPage.clicked.connect(lambda: webbrowser.open(
            self.tr(r'https://qm.qq.com/cgi-bin/qm/qr?k=DgiFh5cclAElnELH4mOxqWUBxReyEVpm&jump_from=webapi')))
        self.tipButton.clicked.connect(lambda: SponsorDialog(platfm))

        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)
        self.masterLayout.addWidget(self.openHelpFileButton)
        self.masterLayout.addWidget(self.openVideoHelpButtone)
        self.masterLayout.addWidget(self.openGiteePage)
        self.masterLayout.addWidget(self.openGithubPage)
        self.masterLayout.addWidget(self.linkToDiscussPage)
        self.masterLayout.addWidget(self.tipButton)

    def openHelpDocument(self):
        try:
            if self.platfm == 'Darwin':
                import shlex
                os.system("open " + shlex.quote(self.tr("./misc/README_zh.html")))
            elif self.platfm == 'Windows':
                os.startfile(os.path.realpath(self.tr('./misc/README_zh.html')))
        except:
            pass