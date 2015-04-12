from PySide.QtGui import *
from PySide.QtCore import *

styleSheet = '''
QWidget {
    background: #002B36;
}
'''

text = open(r'main.py').read().decode('utf-8')
font = QFont('Consolas', 11)

class Widget(QDialog):

    def __init__(self, parent=None):
        super(Widget, self).__init__(parent, Qt.FramelessWindowHint)
        self.setWindowTitle('eno')
        self.setStyleSheet(styleSheet)
        self.doc = QTextDocument()

        fmt = QTextCharFormat()
        fmt.setForeground(QBrush(QColor('#7C8E91')))
        fmt.setFont(font)

        c = QTextCursor(self.doc)
        c.insertText(text, fmt)

    def paintEvent(self, ev):
        p = QPainter(self)

        # draw window border
        pen = p.pen()
        pen.setColor(QColor('#C4D2FF'))
        p.setPen(pen)
        p.drawRect(self.rect().adjusted(0, 0, -1, -1))

        # draw text
        self.doc.drawContents(p)
