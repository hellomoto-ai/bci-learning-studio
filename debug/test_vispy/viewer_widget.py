from PyQt5 import QtCore, QtWidgets

from viewer_widget_ui import Ui_ViewerWidget
from filter_designer import FilterDesigner


def _get_designer(parent, on_change, on_reject):
    filter_designer = FilterDesigner(parent=parent)
    filter_designer.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    filter_designer.changed.connect(on_change)
    filter_designer.rejected.connect(on_reject)
    return filter_designer


class ViewerWidget(QtWidgets.QWidget):
    seek_bar_dragged = QtCore.pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.ui = Ui_ViewerWidget()
        self.ui.setupUi(self)

        self.ui.configureFilter.clicked.connect(self._launch_filter_config)
        self.ui.clearFilter.clicked.connect(self._clear_filter)

        self._filter_params_prev = None
        self._filter_designer = None

    def _emit_event(self, event):
        if event['type'] == 'seek_bar':
            self.seek_bar_dragged.emit(event['value'])

    def initialize(self, n_plots, interactive):
        self.ui.plotter.initialize(n_plots, interactive)
        self.ui.plotter.ui_event.connect(self._emit_event)

    def set_data(self, eeg_data):
        self.ui.plotter.set_data(eeg_data)

    def plot(self, eeg_data):
        self.ui.plotter.set_data(eeg_data)
        self.ui.plotter.reset_range()

    def _launch_filter_config(self):
        self._filter_params_prev = self.ui.plotter.filter_params
        self._filter_designer = _get_designer(
            self, self.set_filter, self._set_previous_filter)
        self._filter_designer.show()
        self._filter_designer.plot()

    def set_filter(self, filter_params):
        self.ui.plotter.set_filter(filter_params)

    def _set_previous_filter(self):
        self.set_filter(self._filter_params_prev)

    def _clear_filter(self):
        self.set_filter(None)
