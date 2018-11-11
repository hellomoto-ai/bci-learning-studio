import logging

import serial
import serial.tools.list_ports
from PyQt5 import QtCore, QtWidgets

from .device_selector_ui import Ui_DeviceSelector

_LG = logging.getLogger(__name__)


def _get_devices():
    return [p.device for p in serial.tools.list_ports.comports()]


def _get_last_used_device():
    settings = QtCore.QSettings('bci_learning_studio', 'device_selector')
    return settings.value('last_used_device', type=str)


def _set_last_used_device(device):
    settings = QtCore.QSettings('bci_learning_studio', 'device_selector')
    settings.setValue('last_used_device', device)


class DeviceSelector(QtWidgets.QDialog):
    message = QtCore.pyqtSignal(str)
    detected = QtCore.pyqtSignal(str, str)

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.ui = Ui_DeviceSelector()
        self.ui.setupUi(self)

        prev = _get_last_used_device()
        self.ui.deviceList.addItems(_get_devices())
        self.ui.deviceList.setCurrentIndex(self.ui.deviceList.findText(prev))
        self.ui.connectButton.clicked.connect(self._connect)

    def _connect(self):
        device = self.ui.deviceList.currentText()
        self.message.emit('Checking %s ...' % device)
        try:
            ser = serial.Serial(port=device, baudrate=115200, timeout=2)
        except Exception:  # pylint: disable=broad-except
            message = 'Failed to open serial connection; %s' % device
            _LG.exception(message)
            self.message.emit(message)
            return

        try:
            ser.write(b'v')
            message = ser.read_until(b'$$$').decode('utf-8', errors='ignore')
        except Exception:  # pylint: disable=broad-except
            message = 'Failed to fetch board info from %s' % device
            _LG.exception(message)
            self.message.emit(message)
            return
        finally:
            ser.close()

        if not message.endswith('$$$'):
            self.message.emit('Failed to fetch board info.')
            return

        if 'ADS1299' in message:
            board_type = 'Cyton'
        else:
            self.message.emit('Unexpected board. %s' % message)
            return

        _set_last_used_device(device)
        self.message.emit('Detected board type; %s' % board_type)
        self.detected.emit(device, board_type)
        self.close()
