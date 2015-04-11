import sys
import subprocess

from PySide.QtGui import *
from PySide.QtCore import *

import config
from view import View
from console import Console

class Widget(QDialog):

    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)

        self.View = View(config.enosPath)
        self.console = Console()

        self.View.setFocusPolicy(Qt.StrongFocus)

        lt = QVBoxLayout()
        lt.addWidget(self.View)
        lt.addWidget(self.console)
        self.setLayout(lt)

        self.View.focusOut.connect(self.switchFocus)

        # fake View's focus out
        self.View.focusOutEvent('')
        self.console.setFocus()
        self.focus = 'console'
        self.console.focusOut.connect(self.switchFocus)

    def keyPressEvent(self, ev):
        ch = ev.text()
        super(Widget, self).keyPressEvent(ev)

    def switchFocus(self):
        if self.focus == 'console':
            self.View.setFocus()
            self.focus = 'View'
        else:
            self.console.setFocus()
            self.focus = 'console'

app = QApplication(sys.argv)
w = Widget()
w.resize(480, 640)
w.show()
app.exec_()
