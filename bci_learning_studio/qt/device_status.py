import time

from PyQt5 import QtWidgets

from .device_status_ui import Ui_DeviceStatus


class DeviceStatus(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_DeviceStatus()
        self.ui.setupUi(self)

        self.ui.boardInfo.viewport().setAutoFillBackground(False)

        self._buffer = []
        self._last_update = 0

    def set_board_info(self, board_info):
        self.ui.boardInfo.setText(board_info)

    def set_sample_rate(self, sample_rate):
        self.ui.sampleRate.setText('%.2f' % sample_rate)

    def tick(self, sample):
        self._buffer.append(sample['timestamp'])
        self._buffer = self._buffer[-1000:]

        now = time.time()
        if now - self._last_update > 0.1 and len(self._buffer) > 10:
            elapsed = self._buffer[-1] - self._buffer[0]
            sample_rate = len(self._buffer) / elapsed
            self.set_sample_rate(sample_rate)
            self._last_update = now
