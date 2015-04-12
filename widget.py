from PySide.QtGui import *
from PySide.QtCore import *

styleSheet = '''
QWidget {
    background: #002B36;
}
'''

text = open(r'main.py').read().decode('utf-8')

class Widget(QDialog):

    def __init__(self, parent=None):
        super(Widget, self).__init__(parent, Qt.FramelessWindowHint)
        self.setWindowTitle('eno')
        self.setStyleSheet(styleSheet)

    def paintEvent(self, ev):
        p = QPainter(self)
        pen = p.pen()
        pen.setColor(QColor('#C4D2FF'))
        p.setPen(pen)
        p.drawRect(self.rect().adjusted(0, 0, -1, -1))

        p.drawText(100, 100, text)
