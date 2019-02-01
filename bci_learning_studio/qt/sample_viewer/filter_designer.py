import numpy as np
import scipy.signal
from PyQt5 import QtWidgets, QtCore
import vispy.app
import vispy.gloo

from .filter_designer_ui import Ui_filterDesigner
from bci_learning_studio.qt import vispy_util


def _init_btype_selector(combo_box):
    for type_ in ['lowpass', 'highpass', 'bandpass', 'bandstop']:
        combo_box.addItem(type_.capitalize(), type_)
    combo_box.setCurrentIndex(2)


def _get_butter_response(wn, n_order, btype):
    fs = np.mean(wn) * 4
    b, a = scipy.signal.butter(
        n_order, wn, btype=btype, analog=False, fs=fs)
    w, h = scipy.signal.freqz(b, a)
    x = (fs * 0.5 / np.pi) * w
    y = abs(h)
    return x, y


def _get_plot(filter_params):
    if filter_params['type'] == 'butter':
        return _get_butter_response(**filter_params['params'])
    raise ValueError('Unexpected filter type; %s' % filter_params['type'])


def _init_plot(widget, max_axis_width=40):
    viewbox = vispy.scene.ViewBox(camera='panzoom')
    line = vispy.scene.visuals.Line(np.array([[0, 0]]), color='w')
    viewbox.add(vispy.scene.visuals.GridLines())
    viewbox.add(line)

    yaxis = vispy_util.get_axis(orientation='left')
    yaxis.width_max = max_axis_width

    xaxis = vispy_util.get_axis(orientation='bottom')
    xaxis.height_max = max_axis_width
    grid = widget.add_grid()
    grid.add_widget(yaxis, row=0, col=0)
    grid.add_widget(xaxis, row=1, col=1)
    grid.add_widget(viewbox, row=0, col=1)

    yaxis.link_view(viewbox)
    xaxis.link_view(viewbox)
    return viewbox, line


class _Plotter(vispy.scene.SceneCanvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.unfreeze()
        self.viewbox, self.line = _init_plot(self.central_widget)

    def _process_mouse_event(self, event):
        event.handled = True

    def plot(self, x, y):
        self.line.set_data(pos=np.vstack((x, y)).T)
        self.viewbox.camera.set_range()


def _make_plotter(widget):
    layout = QtWidgets.QVBoxLayout()
    plotter = _Plotter()
    layout.addWidget(plotter.native)
    widget.setLayout(layout)
    return plotter


class FilterDesigner(QtWidgets.QDialog):
    changed = QtCore.pyqtSignal('PyQt_PyObject')

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.ui = Ui_filterDesigner()
        self.ui.setupUi(self)

        self._plotter = _make_plotter(self.ui.plotter)

        _init_btype_selector(self.ui.bandTypeSelector)
        self.ui.filterOrder.setValue(2)
        self.ui.criticalFreq.setValue(60)
        self.ui.bandWidth.setValue(20)

        self.ui.bandTypeSelector.activated.connect(self.plot)
        self.ui.bandTypeSelector.activated.connect(self._disable_bandwidth)
        self.ui.filterOrder.valueChanged.connect(self.plot)
        self.ui.criticalFreq.valueChanged.connect(self.plot)
        self.ui.bandWidth.valueChanged.connect(self.plot)

    def _disable_bandwidth(self):
        btype = self.ui.bandTypeSelector.currentData()
        self.ui.bandWidth.setEnabled(btype in ['bandpass', 'bandstop'])

    def plot(self):
        filter_params = self._get_filter_params()
        x, y = _get_plot(filter_params)
        self._plotter.plot(x, y)
        self.changed.emit(filter_params)

    def _get_filter_params(self):
        btype = self.ui.bandTypeSelector.currentData()
        n_order = self.ui.filterOrder.value()
        critical_freq = self.ui.criticalFreq.value()
        if btype in ['lowpass', 'highpass']:
            wn = critical_freq
        else:
            band_width = self.ui.bandWidth.value()
            wn = [
                critical_freq - band_width / 2,
                critical_freq + band_width / 2,
            ]
        return {
            'type': 'butter',
            'params': {
                'btype': btype, 'wn': wn, 'n_order': n_order
            },
        }
