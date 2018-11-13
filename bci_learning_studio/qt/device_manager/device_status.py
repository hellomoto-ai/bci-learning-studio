"""Device status shows board information and read time sampling rate"""
from PyQt5 import QtWidgets

from .device_status_ui import Ui_DeviceStatus


class DeviceStatus(QtWidgets.QWidget):
    """Show board status"""
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_DeviceStatus()
        self.ui.setupUi(self)

        self.ui.boardInfo.viewport().setAutoFillBackground(False)

        self._buffer = []
        self._last_update = 0

    def init(self, board_info=''):
        """Initialize board information and sampling rate buffer"""
        self._set_sample_rate(0)
        self.ui.boardInfo.setText(board_info)

    def _set_sample_rate(self, sample_rate):
        self.ui.sampleRate.setText('%.2f' % sample_rate)

    def tick(self, sample):
        """Add sample timestamp to buffer and update sample rate label"""
        latest = sample['timestamp']
        self._buffer.append(latest)
        self._buffer = self._buffer[-1000:]

        if latest - self._last_update > 0.1 and len(self._buffer) > 10:
            sample_rate = (len(self._buffer) - 1) / (latest - self._buffer[0])
            self._set_sample_rate(sample_rate)
            self._last_update = latest
