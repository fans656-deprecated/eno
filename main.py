from PySide.QtGui import *
from PySide.QtCore import *

import sys
import os
import re
import subprocess

import config

def isIgnored(f):
    return any((lambda r: re.match(r, f))(r) for r in config.ignores)

class ListView(QListWidget):

    focusOut = Signal()

    def __init__(self, path, parent=None):
        super(ListView, self).__init__(parent)
        self.setFont(QFont('Inconsolata', 14))
        self.basepath = path
        self.enterDir(self.basepath)

    def enterDir(self, path):
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
        self.populate(dirs, files)

    def populate(self, dirs, files):
        self.dirs = dirs
        self.files = files
        self.items = dirs + files
        self.clear()
        for name, path in dirs:
            self.addItem('/' + name)
        for name, path in files:
            if name.endswith('txt'):
                name = name[:-4]
            self.addItem(name)
        self.nDirs = len(dirs)
        self.nFiles = len(files)
        self.nTotal = self.nDirs + self.nFiles
        self.setCurrentRow(self.nTotal // 2)

    def nav(self, d):
        i = self.currentRow()
        i = (i + d + self.nTotal) % self.nTotal
        self.setCurrentRow(i)

    def navPrev(self):
        self.nav(-1)

    def navNext(self):
        self.nav(1)

    def navUp(self):
        if self.curpath != self.basepath:
            self.enterDir(os.path.abspath(os.path.join(self.curpath, '..')))

    def enter(self):
        i = self.currentRow()
        item = self.items[i]
        name, path = item
        if os.path.isdir(path):
            self.enterDir(path)
        else:
            self.openFile(path)

    def openFile(self, path):
        print u'open file {}'.format(path)
        subprocess.call(u'gvim {}'.format(path).encode('gbk'), shell=True)

    def keyPressEvent(self, ev):
        ch = ev.text()
        if ch == config.ch_switch_focus:
            self.focusOut.emit()
        elif ch == config.ch_prev:
            self.navPrev()
        elif ch == config.ch_next:
            self.navNext()
        elif ch == config.ch_up:
            self.navUp()
        elif ch == config.ch_enter:
            self.enter()
        else:
            super(ListView, self).keyPressEvent(ev)

    def focusInEvent(self, ev):
        self.setStyleSheet('QListWidget{background: #B5BDFF}')

    def focusOutEvent(self, ev):
        self.setStyleSheet('QListWidget{background: #BDBDBD}')

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

class Widget(QDialog):

    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)

        self.listView = ListView(config.enosPath)
        self.console = Console()

        self.listView.setFocusPolicy(Qt.StrongFocus)

        lt = QVBoxLayout()
        lt.addWidget(self.listView)
        lt.addWidget(self.console)
        self.setLayout(lt)

        self.listView.focusOut.connect(self.switchFocus)

        # fake listview's focus out
        self.listView.focusOutEvent('')
        self.console.setFocus()
        self.focus = 'console'
        self.console.focusOut.connect(self.switchFocus)

    def keyPressEvent(self, ev):
        ch = ev.text()
        super(Widget, self).keyPressEvent(ev)

    def switchFocus(self):
        if self.focus == 'console':
            self.listView.setFocus()
            self.focus = 'listview'
        else:
            self.console.setFocus()
            self.focus = 'console'

app = QApplication(sys.argv)
w = Widget()
w.resize(480, 640)
w.show()
app.exec_()
