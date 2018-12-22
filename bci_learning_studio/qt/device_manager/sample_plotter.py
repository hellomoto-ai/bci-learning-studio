import logging

from PyQt5 import QtCore, QtWidgets
import pyqtgraph

from bci_learning_studio.qt import qt_util
from .sample_plotter_ui import Ui_SamplePlotter

_LG = logging.getLogger(__name__)


class SamplePlotter(QtWidgets.QMainWindow):
    closed = QtCore.pyqtSignal()

    def __init__(self, parent, history=250 * 3):
        super().__init__(parent=parent)
        self.ui = Ui_SamplePlotter()
        self.ui.setupUi(self)

        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self._plot)
        self._timer.setInterval(100)

        self.history = history
        self._buffer = []
        self._lines = []
        self._plots = []

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
        self._buffer = []
        self._lines = []
        self._plots = []
        self.ui.graphWidget.clear()

    def append(self, sample):
        eeg = sample['data']['eeg']
        if len(self._buffer) != len(eeg):
            self._buffer = [[0.0] * self.history] * len(eeg)

        for i, val in enumerate(eeg):
            self._buffer[i].append(val)
            self._buffer[i] = self._buffer[i][1:]

    def _plot(self):
        if len(self._lines) != len(self._buffer):
            self._init_plot()
        for line, data in zip(self._lines, self._buffer):
            line.setData(data)

    def _init_plot(self):
        self.ui.graphWidget.clear()
        title = 'Channels'
        plot = self.ui.graphWidget.addPlot(row=1, col=1, title=title)
        self._plots.append(plot.showGrid(x=True, y=True, alpha=1))
        for _ in range(len(self._buffer)):
            line = plot.plot([], pen=pyqtgraph.mkPen(color=(0, 0, 255)))
            self._lines.append(line)
