#!/usr/bin/env python
from PyQt5 import QtWidgets

import numpy as np
import vispy.app

from viewer_widget import ViewerWidget


def _load_data(sample_rate=250, n_channels=16, n_samples=10000):
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


def _main():
    app = QtWidgets.QApplication([])

    window = QtWidgets.QMainWindow()
    widget = ViewerWidget()
    widget.initialize(n_plots=16, interactive=True)
    window.setCentralWidget(widget)

    widget.plot(**_load_data())
    def update(_):
        widget.set_data(**_load_data())
    timer = vispy.app.Timer(interval=1/15, connect=update, start=True)

    window.show()
    app.exec_()


if __name__ == '__main__':
    _main()
