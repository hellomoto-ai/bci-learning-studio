import time
import logging

from PyQt5 import QtGui, QtCore

from .DeviceControllerWidget_Ui import Ui_DeviceControllerWidget
from .PlotWindow import PlotWindow

_LG = logging.getLogger(__name__)


class SampleAcquisitionThread(QtCore.QThread):
    acquired = QtCore.pyqtSignal('PyQt_PyObject')

    def __init__(self):
        super().__init__()
        self._board = None
        self._stop_requested = False

    def set_board(self, board):
        self._board = board

    def run(self):
        _LG.info('Starting sample acquisition thread.')
        self._stop_requested = False
        while not self._stop_requested:
            try:
                sample = self._board.read_sample()
                self.acquired.emit(sample)
            except Exception:  # pylint: disable=broad-except
                _LG.exception('failed to fetch')
            finally:
                time.sleep(0.5 / 250)

    def stop(self):
        _LG.info('Stopping sample acquisition thread.')
        self._stop_requested = True


class DeviceControllerWidget(QtGui.QWidget, Ui_DeviceControllerWidget):
    sample_acquired = QtCore.pyqtSignal('PyQt_PyObject')

    def __init__(self, parent=None):
        super(DeviceControllerWidget, self).__init__(parent)
        self.setupUi(self)
        self._board = None
        self._last_acquired = None
        self._n_acquired = 0
        self._data = []
        self._plots = []
        self._last_plot = None
        self.streaming = False

        self.pushButtonStreaming.clicked.connect(self.start_streaming)
        self.pushButtonPlot.toggled.connect(self._toggle_plot)
        self.sample_acquisition = SampleAcquisitionThread()
        self.sample_acquisition.acquired.connect(self._sample_acquired)
        self.sample_acquisition.acquired.connect(self._update_plot)
        self.plot_window = None

    def set_board(self, board):
        self._board = board
        self.textEditDeviceProertry.setText(self._board.initialize())
        self.sample_acquisition.set_board(board)

    def start_streaming(self):
        self._board.start_streaming()
        self.pushButtonStreaming.clicked.disconnect(self.start_streaming)
        self.pushButtonStreaming.clicked.connect(self.stop_streaming)
        self.pushButtonStreaming.setText('Stop Streaming')
        self.sample_acquisition.start()
        self.streaming = True
        self._last_acquired = time.time()
        self._n_acquired = 0

    def stop_streaming(self):
        if self.plot_window:
            self.close_plot()
        self._board.stop_streaming()
        self.pushButtonStreaming.clicked.disconnect(self.stop_streaming)
        self.pushButtonStreaming.clicked.connect(self.start_streaming)
        self.pushButtonStreaming.setText('Start Streaming')
        self.sample_acquisition.stop()
        self.streaming = False

    def _sample_acquired(self, value):
        self.sample_acquired.emit(value)
        self._n_acquired += 1
        now = time.time()
        elapsed = now - self._last_acquired
        if elapsed > 0.7:
            rate = self._n_acquired / elapsed
            self.lineEditRate.setText('%s Hz' % int(rate))
            self._last_acquired = now
            self._n_acquired = 0

    def _toggle_plot(self, checked):
        if checked:
            self.open_plot()
        else:
            self.close_plot()

    def open_plot(self):
        self.plot_window = PlotWindow()
        self.plot_window.show()

        for i in range(self._board.num_eeg):
            data = [0.0] * (250 * 7)
            plot = self.plot_window.plotWidget.addPlot(
                row=i, col=0, title='EEG Channel %s' % i)
            curve = plot.plot(data)
            self._data.append(data)
            self._plots.append(curve)
        self._last_plot = time.time()

    def _update_plot(self, sample):
        if not self._plots:
            return
        for i in range(self._board.num_eeg):
            self._data[i].append(sample['eeg'][i])
            self._data[i] = self._data[i][1:]
        now = time.time()
        if now - self._last_plot > 0.04:
            for i in range(self._board.num_eeg):
                self._plots[i].setData(self._data[i])
            self._last_plot = now

    def close_plot(self):
        self.plot_window.close()
        self.plot_window = None
        self._data = []
        self._plots = []
