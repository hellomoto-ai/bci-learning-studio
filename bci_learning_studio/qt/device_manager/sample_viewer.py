import logging

import numpy as np
from PyQt5 import QtCore, QtWidgets

from bci_learning_studio.qt import qt_util
from .sample_viewer_ui import Ui_SampleViewer

_LG = logging.getLogger(__name__)


class SampleViewer(QtWidgets.QMainWindow):
    closed = QtCore.pyqtSignal()

    def __init__(self, parent, n_samples=250*10):
        super().__init__(parent=parent)
        self.ui = Ui_SampleViewer()
        self.ui.setupUi(self)
        self.ui.viewer.init_plotter(interactive=False)

        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self._plot)
        self._timer.setInterval(100)

        self.n_samples = n_samples
        self._eeg_data = {
            'sample_rate': None,
            'timestamps': [],
            'samples': [],
        }

        qt_util.restore_window_position(self)

    def showEvent(self, event):
        self._timer.start()
        event.accept()

    def hideEvent(self, event):
        self._timer.stop()
        event.accept()

    def closeEvent(self, event):
        qt_util.store_window_position(self)
        event.accept()

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Escape:
            self.close()

    def reset(self):
        self._eeg_data = {
            'sample_rate': None,
            'timestamps': [],
            'samples': [],
        }

    def append(self, sample):
        if sample['type'] != 'eeg':
            return
        data = sample['data']
        self._eeg_data['sample_rate'] = data['sampling_rate']
        self._eeg_data['timestamps'].append(data['timestamp'])
        self._eeg_data['samples'].append(data['eeg'])

        self._eeg_data['timestamps'] = (
            self._eeg_data['timestamps'][-self.n_samples:])
        self._eeg_data['samples'] = (
            self._eeg_data['samples'][-self.n_samples:])

    def _plot(self):
        if not self._eeg_data['sample_rate']:
            return
        eeg_data = {
            'sample_rate': self._eeg_data['sample_rate'],
            'timestamps': np.asarray(self._eeg_data['timestamps']),
            'samples': np.asarray(self._eeg_data['samples']).T,
        }
        self.ui.viewer.plot(eeg_data)
