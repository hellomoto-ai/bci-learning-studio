"""DeviceSelector lets user pick a serial device and cache the last choice."""
import logging

import serial.tools.list_ports
from PyQt5 import QtCore, QtWidgets

from bci_learning_studio.qt import qt_util
from .device_selector_ui import Ui_DeviceSelector

_LG = logging.getLogger(__name__)


def _get_devices():
    return [p.device for p in serial.tools.list_ports.comports()]


class DeviceSelector(QtWidgets.QDialog):
    """Setup Dialog for selecting a device from serial port list"""
    selected = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent=parent)

        self.ui = Ui_DeviceSelector()
        self.ui.setupUi(self)
        self.ui.deviceList.addItems(_get_devices())
        self.ui.connectButton.clicked.connect(self._selected)

        prev = qt_util.get_settings('last_used_device')
        self.ui.deviceList.setCurrentIndex(self.ui.deviceList.findText(prev))

    def _selected(self):
        device = self.ui.deviceList.currentText()
        if device:
            qt_util.store_settings(last_used_device=device)
            self.selected.emit(device)
