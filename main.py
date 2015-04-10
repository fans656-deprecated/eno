from PySide.QtGui import *
from PySide.QtCore import *

import sys
import os
import re

import config

def isIgnored(f):
    return any((lambda r: re.match(r, f))(r) for r in config.ignores)

class ListView(QListWidget):

    def __init__(self, parent=None):
        super(ListView, self).__init__(parent)
        self.setFont(QFont('Inconsolata', 14))

    def populate(self, dirs, files):
        self.dirs = dirs
        self.files = files
        self.clear()
        for name, path in dirs:
            self.addItem('/' + name)
        for name, path in files:
            if name.endswith('txt'):
                name = name[:-4]
            self.addItem(name)

class Console(QLineEdit):

    pass

class Widget(QDialog):

    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)

        self.listView = ListView()
        self.console = Console()

        lt = QVBoxLayout()
        lt.addWidget(self.listView)
        lt.addWidget(self.console)
        self.setLayout(lt)

        self.basepath = config.enosPath
        self.cd(self.basepath)

    def cd(self, path):
        self.curpath = path
        dirs = []
        files = []
        for t in os.listdir(path):
            if isIgnored(t): continue
            tpath = os.path.join(path, t)
            if os.path.isdir(tpath):
                dirs.append((t, tpath))
            else:
                files.append((t, tpath))
        dirs = sorted(dirs, key=lambda t: t[0])
        files = sorted(files, key=lambda t: t[0])

        self.listView.populate(dirs, files)

app = QApplication(sys.argv)
w = Widget()
w.resize(480, 640)
w.show()
app.exec_()
