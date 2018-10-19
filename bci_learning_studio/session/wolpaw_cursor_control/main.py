import logging

from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor

from .WolpawCursorControl import WolpawCursorControl

_LG = logging.getLogger(__name__)


def main(args):
    app = QtWidgets.QApplication(args)
    _main = WolpawCursorControl()
    _main.show()
    app.exec_()
