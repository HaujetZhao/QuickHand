from PySide2.QtWidgets import *
from PySide2.QtGui import *
class ColorLabel(QLabel):

    palette = QPalette()
    color = QColor()
    color.setRgb(0,0,0)


    def __init__(self, text):
        super().__init__()
        self.setText(text)
        self.setAutoFillBackground(True)
        self.setColor()

    def mousePressEvent(self, ev:QMouseEvent):
        self.color = QColorDialog.getColor()
        self.palette.setColor(QPalette.Window, self.color)
        self.setColor()

    def setColor(self):
        self.palette.setColor(QPalette.Window, self.color)
        self.setPalette(self.palette)