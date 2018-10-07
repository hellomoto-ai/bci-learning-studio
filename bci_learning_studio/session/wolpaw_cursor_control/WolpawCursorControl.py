from PyQt5 import QtWidgets

from .WolpawCursorControl_Ui import Ui_WolpawCursorControl


class WolpawCursorControl(QtWidgets.QMainWindow, Ui_WolpawCursorControl):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

