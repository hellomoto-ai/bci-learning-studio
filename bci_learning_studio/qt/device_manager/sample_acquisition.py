import time
import logging

import serial
from PyQt5 import QtCore

_LG = logging.getLogger(__name__)


class SampleAcquisitionThread(QtCore.QThread):
    acquired = QtCore.pyqtSignal('PyQt_PyObject')

    def __init__(self, board, wait_factor=0.85):
        super().__init__()
        self._board = board
        self.wait_factor = wait_factor

    def run(self):
        _LG.info('Starting sample acquisition thread.')

        # `cycle` here is a sensitive value;
        # Setting it same as (1.0 * board.cycle) will cause sample acquisition
        # out of sync (delayed) and you will see end byte not matching to
        # expected value -> wrong value.
        # Setting it to (0.5 * board.cycle) will cause sample acquisition
        # too quick so that sample distribution over time is skewed.
        #
        # 0.85 was found okay in the sense that it does not cause wrong
        # end byte while sample distribution over time is kind of smooth.
        cycle = self.wait_factor * self._board.cycle
        unit_wait = cycle / 10.0
        last_acquired = time.monotonic()
        while self._board.streaming:
            now = time.monotonic()
            if now - last_acquired < cycle:
                self.sleep(unit_wait)
                continue
            try:
                sample = self._board.read_sample()
                if sample['valid']:
                    self.acquired.emit({'type': 'eeg', 'data': sample})
                last_acquired = now
            except serial.serialutil.SerialException:
                _LG.info('Connection seems to be closed.')
            except Exception:  # pylint: disable=broad-except
                _LG.exception('failed to fetch')
        _LG.info('Sample acquisition thread stopped.')
