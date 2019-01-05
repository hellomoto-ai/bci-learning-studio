import scipy.signal
from PyQt5 import QtWidgets, QtCore

from .viewer_ui import Ui_viewer
from .filter_designer import FilterDesigner


def _get_butter_filter(sample_rate, btype, wn, n_order):
    return scipy.signal.butter(
        n_order, wn, btype=btype, analog=False, fs=sample_rate)


def _apply_filter(data, filter_params, sample_rate):
    if filter_params['type'] == 'butter':
        b, a = _get_butter_filter(sample_rate, **filter_params['params'])
    else:
        raise ValueError('Unexpected filter type; %s' % filter_params['type'])
    return scipy.signal.lfilter(b, a, data, axis=1)


class ViewerWidget(QtWidgets.QWidget):
    seek_bar_dragged = QtCore.pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_viewer()
        self.ui.setupUi(self)

        self.ui.configureFilter.clicked.connect(self._launch_filter_config)
        self.ui.clearFilter.clicked.connect(self._clear_filter)

        self._eeg_data = None
        self._event_data = None

        self._filter_params = None
        self._filter_params_prev = None
        self._filter_designer = None

    def plot(self, eeg_data, event_data=None):
        self._eeg_data = eeg_data
        self._event_data = event_data
        self._plot()

    def _plot(self):
        if not self._eeg_data:
            return
        x, ys = self._eeg_data['timestamps'], self._eeg_data['samples']
        if self._filter_params:
            ys = _apply_filter(
                ys, self._filter_params, self._eeg_data['sample_rate'])
        self.ui.plotter.setData(x, ys)
        if self._event_data:
            self.ui.plotter.plot_event(self._event_data['timestamps'])
        self.ui.plotter.seek_bar_dragged.connect(self._seek_bar_dragged)

    def _seek_bar_dragged(self, x):
        self.seek_bar_dragged.emit(x)

    def _launch_filter_config(self):
        self._filter_params_prev = self._filter_params
        self._filter_designer = FilterDesigner(parent=self)
        self._filter_designer.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self._filter_designer.changed.connect(self._update_plot)
        self._filter_designer.rejected.connect(self._set_previous_filter)
        self._filter_designer.show()
        self._filter_designer.plot()

    def _update_plot(self, filter_params):
        self._filter_params = filter_params
        self._plot()

    def _set_previous_filter(self):
        self._filter_params = self._filter_params_prev
        self._plot()

    def _clear_filter(self):
        self._filter_params = None
        self._plot()
