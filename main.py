# coding: utf-8
import sys

from PySide.QtGui import *
from PySide.QtCore import *

from widget import Widget

app = QApplication(sys.argv)
availGeo = QApplication.desktop().availableGeometry()

w = Widget()
w.show()
w.resize(640, 480)
w.move(availGeo.width() - w.width(), availGeo.height() - w.height())

app.exec_()
