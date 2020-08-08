from PySide2.QtCore import *
from PIL import Image
from handright import Template, handwrite

class GenerateImagesThread(QThread):
    text = None
    template = None
    outputPath = None
    signal = Signal(str)
    showImage = False

    def __init__(self, parent=None):
        super(GenerateImagesThread, self).__init__(parent)

    def print(self, text):
        self.signal.emit(text)

    def run(self):
        self.signal.emit('开始生成图片\n\n')
        try:
            images = handwrite(self.text, self.template)
            for i, im in enumerate(images):
                assert isinstance(im, Image.Image)
                self.signal.emit('第 %s 张图片生成\n\n' % str(int(i) + 1))
                if self.showImage == True:
                    im.show()
                outputDir = self.outputPath.replace('\\', '/')
                im.save(outputDir + "/{}.webp".replace('//', '/').format(i))
            self.signal.emit('所有图片生成完毕，输出文件夹为：%s\n\n' % outputDir)
        except Exception as e:
            self.signal.emit('出错了，报错信息如下：\n\n')
            self.signal.emit(str(e) + '\n\n')
