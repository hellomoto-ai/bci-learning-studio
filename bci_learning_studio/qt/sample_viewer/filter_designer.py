import numpy as np
import scipy.signal
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg

from .filter_designer_ui import Ui_filterDesigner


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


class FilterDesigner(QtWidgets.QDialog):
    changed = QtCore.pyqtSignal('PyQt_PyObject')

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.ui = Ui_filterDesigner()
        self.ui.setupUi(self)

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

        self.ui.plotter.clear()
        self.ui.plotter.setBackground('w')
        self.ui.plotter.plot(x, y, pen=pg.mkPen('k', width=2))
        self.ui.plotter.setMouseEnabled(False, False)
        self.ui.plotter.showGrid(x=True, y=True)
        self.ui.plotter.setLabel(axis='bottom', text='Freq', units='Hz')
        self.ui.plotter.setLabel(axis='left', text='Gain')

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
