import logging

from PyQt5 import QtCore, QtWidgets

from bci_learning_studio.qt import qt_util
from .sample_plotter_ui import Ui_SamplePlotter

_LG = logging.getLogger(__name__)


class SamplePlotter(QtWidgets.QMainWindow):
    closed = QtCore.pyqtSignal()

    def __init__(self, parent, history=250 * 7):
        super().__init__(parent=parent)
        self.ui = Ui_SamplePlotter()
        self.ui.setupUi(self)

        self._timer = None

        self.history = history
        self._buffer = []
        self._lines = []
        self._plots = []

        qt_util.restore_window_position(self)

    def showEvent(self, event):
        self._timer = qt_util.PeriodicCall(fps=10)
        self._timer.elapsed.connect(self._plot)
        self._timer.start()
        event.accept()

    def hideEvent(self, event):
        self._timer.stop()
        del self._timer
        self._timer = None
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
        eeg = sample['eeg']
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
        for i in range(len(self._buffer)):
            row = i % 8
            col = i // 8
            title = 'Channel %s' % (i + 1)
            plot = self.ui.graphWidget.addPlot(row=row, col=col, title=title)
            line = plot.plot([])
            self._plots.append(plot)
            self._lines.append(line)
