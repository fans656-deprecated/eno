import sys

from PySide.QtGui import *
from PySide.QtCore import *

from widget import Widget

app = QApplication(sys.argv)
w = Widget()
w.show()
app.exec_()
