"""Device status shows board information and read time sampling rate"""
from PyQt5 import QtWidgets

from .device_status_ui import Ui_DeviceStatus


_RAILED_THREASHOLD = int(pow(2, 23) - 1000)
_NEAR_RAILED_THREASHOLD = int(pow(2, 23) * 0.9)


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
        self.ui.measurementStatusIndicator.reset_status()

    def _set_sample_rate(self, sample_rate):
        self.ui.sampleRate.setText('%.2f' % sample_rate)

    def _update_indicator(self, raw_eeg):
        if any(abs(val) > _RAILED_THREASHOLD for val in raw_eeg):
            self.ui.measurementStatusIndicator.set_railed()
        elif any(abs(val) > _NEAR_RAILED_THREASHOLD for val in raw_eeg):
            self.ui.measurementStatusIndicator.set_near_railed()
        else:
            self.ui.measurementStatusIndicator.set_ok()
        self.ui.measurementStatusIndicator.update()

    def tick(self, sample):
        """Add sample timestamp to buffer and update sample rate label"""
        latest = sample['data']['timestamp']
        self._buffer.append(latest)
        self._buffer = self._buffer[-1000:]

        self._update_indicator(sample['data']['raw_eeg'])

        if latest - self._last_update > 0.1 and len(self._buffer) > 10:
            sample_rate = (len(self._buffer) - 1) / (latest - self._buffer[0])
            self._set_sample_rate(sample_rate)
            self._last_update = latest
