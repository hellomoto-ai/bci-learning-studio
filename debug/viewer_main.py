#!/usr/bin/env python
import numpy as np
from PyQt5 import QtWidgets

from viewer_window_ui import Ui_ViewerWindow


def _load_data():
    sample_rate = 250
    n_channels = 16
    n_samples = 10000

    samples = []
    for i in range(n_channels):
        signal_freq = i * 4
        base_phase = 2 * np.pi * n_samples / sample_rate
        phase = np.linspace(0, base_phase * signal_freq, n_samples)
        samples.append(10 * np.sin(phase) + np.random.random(n_samples))
    samples = np.asarray(samples)

    timestamps = np.asarray([i / sample_rate for i in range(n_samples)])
    return {
        'eeg_data': {
            'sample_rate': sample_rate,
            'timestamps': timestamps,
            'samples': samples,
        },
        'event_data': {
            'timestamps': np.random.random(100) * n_samples / sample_rate
        }
    }


class ViewerWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.ui = Ui_ViewerWindow()
        self.ui.setupUi(self)
        self.ui.sampleViewer.init_plotter(interactive=True)


def _main():
    app = QtWidgets.QApplication([])
    viewer = ViewerWindow()
    viewer.show()
    viewer.ui.sampleViewer.plot(**_load_data())
    app.exec_()


if __name__ == '__main__':
    _main()
