from PyQt5 import QtWidgets

from .DeviceManager_Ui import Ui_DeviceManager


class DeviceManager(QtWidgets.QMainWindow, Ui_DeviceManager):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
