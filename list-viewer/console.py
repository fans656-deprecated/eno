from PySide.QtGui import *
from PySide.QtCore import *

class Console(QLineEdit):

    focusOut = Signal()

    def __init__(self, parent=None):
        super(Console, self).__init__(parent)
        self.textChanged.connect(self.onTextChanged)

    def onTextChanged(self, text):
        if text.startswith(' ') or text.endswith(' '):
            self.focusOut.emit()

    def focusInEvent(self, ev):
        self.setStyleSheet('QLineEdit{background: #fff}')
        self.clear()

    def focusOutEvent(self, ev):
        self.setStyleSheet('QLineEdit{background: #BDBDBD}')
        self.clear()
