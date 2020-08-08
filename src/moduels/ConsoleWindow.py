from PySide2.QtWidgets import *
from PySide2.QtGui import *
from moduels.ConsolePrintBox import ConsolePrintBox


class ConsoleWindow(QMainWindow):
    # 这个 console 是个子窗口，调用的时候要指定父窗口。例如：window = Console(main)
    # 里面包含一个 OutputBox, 可以将信号导到它的 print 方法。
    thread = None

    def __init__(self, parent=None):
        super(ConsoleWindow, self).__init__(parent)
        self.initGui()

    def initGui(self):
        self.setWindowTitle(self.tr('运行信息输出窗口'))
        self.resize(1300, 700)
        self.consolePrintBox = ConsolePrintBox() # 他就用于输出用户定义的打印信息
        self.consolePrintBox.setParent(self)
        self.setCentralWidget(self.consolePrintBox)
        self.show()

    def closeEvent(self, a0: QCloseEvent) -> None:
        try:
            self.thread.exit()
            print('Thread exited')
            self.thread.setTerminationEnabled(True)
            self.thread.terminate()
            print('Thread terminated')
        except:
            pass