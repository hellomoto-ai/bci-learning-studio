import logging

import serial
import serial.tools.list_ports
from PyQt5 import QtCore, QtGui
import openbci_interface.util
from openbci_interface.cyton import Cyton

from .DeviceManagerWidget_Ui import Ui_DeviceManagerWidget

_LG = logging.getLogger(__name__)


def _get_devices():
    return [p.device for p in serial.tools.list_ports.comports()]


class _CheckDevice(QtCore.QThread):  # pylint: disable=too-few-public-methods
    """Check if device is OpenBCI board."""
    detected = QtCore.pyqtSignal('PyQt_PyObject')

    def __init__(self, device):
        super().__init__()
        self.device = device

    def run(self):
        """Query serial device and detect boad type"""
        message = None
        result = None
        try:
            ser = serial.Serial(port=self.device, baudrate=115200, timeout=2)
            board = openbci_interface.util.wrap(ser)
            result = board.__class__.__name__
            message = 'Detected %s.' % result
        except Exception as err:  # pylint: disable=broad-except
            message = str(err)
            _LG.exception('Failed to detect board type.')
        self.detected.emit((self.device, result, message))


_CONNECT_ICON = ':/bci_learning_studio/resource/baseline-phonelink-24px.svg'
_DISCONNECT_ICON = (
    ':/bci_learning_studio/resource/baseline-phonelink_off-24px.svg')


class DeviceManagerWidget(QtGui.QWidget, Ui_DeviceManagerWidget):
    def __init__(self, parent=None):
        super(DeviceManagerWidget, self).__init__(parent)
        # UI
        self.setupUi(self)
        self._refresh_device_list()

        # Signals
        self.pushButtonRefresh.clicked.connect(self._refresh_device_list)
        self.pushButtonConnect.clicked.connect(self._check_device)

        # Other stuff
        self._board = None
        self._checker_thread = None

    def _set_status(self, message):
        self.window().statusBar().showMessage(message)

    def _refresh_device_list(self):
        self.comboBoxDeviceList.clear()
        self.comboBoxDeviceList.addItems(_get_devices())

    def _check_device(self):
        device = self.comboBoxDeviceList.currentText()
        self._set_status('Checking %s' % device)
        self.setEnabled(False)
        self._checker_thread = _CheckDevice(device)
        self._checker_thread.detected.connect(self._initialize_device)
        self._checker_thread.start()

    def _disconnect_device(self):
        if self.DeviceControllerWidget.streaming:
            self.DeviceControllerWidget.stop_streaming()
        self._board.close()
        self._unlock_ui()

    def _lock_ui(self):
        self.DeviceControllerWidget.setEnabled(True)
        self.comboBoxDeviceList.setEnabled(False)
        self.pushButtonRefresh.setEnabled(False)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(_DISCONNECT_ICON),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonConnect.setIcon(icon)
        self.pushButtonConnect.clicked.disconnect(self._check_device)
        self.pushButtonConnect.clicked.connect(self._disconnect_device)

    def _unlock_ui(self):
        self.DeviceControllerWidget.setEnabled(False)
        self.comboBoxDeviceList.setEnabled(True)
        self.pushButtonRefresh.setEnabled(True)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(_CONNECT_ICON),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonConnect.setIcon(icon)
        self.pushButtonConnect.clicked.disconnect(self._disconnect_device)
        self.pushButtonConnect.clicked.connect(self._check_device)

    def _initialize_device(self, signal):
        self.setEnabled(True)
        device, board_type, message = signal
        self._set_status(message)
        if board_type == 'Cyton':
            self._board = Cyton(port=device, baudrate=115200, timeout=2)
        else:
            return

        self._board.open()
        self.DeviceControllerWidget.set_board(self._board)
        self._lock_ui()
