from PySide2.QtWidgets import *
from PySide2.QtGui import *

class SponsorDialog(QDialog):
    def __init__(self, platfm, parent=None):
        super(SponsorDialog, self).__init__(parent)
        self.resize(784, 890)
        if platfm == 'Windows':
            self.setWindowIcon(QIcon('icon.ico'))
        else:
            self.setWindowIcon(QIcon('icon.icns'))
        self.setWindowTitle(self.tr('打赏作者'))
        self.exec()

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap('./sponsor.jpg')
        painter.drawPixmap(self.rect(), pixmap)