#!/usr/bin/env python
import time

import numpy as np
from PyQt5 import QtWidgets

from bci_learning_studio.qt.device_manager.sample_viewer import SampleViewer
from bci_learning_studio.qt.device_manager.sample_acquisition import SampleAcquisitionThread


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


class _BoardMock:
    def __init__(self):
        self.sample_rate = 250
        self.streaming = True
        self.cycle = 1 / self.sample_rate

    def read_sample(self):
        _time = time.time()
        return {
            'valid': True,
            'timestamp': _time,
            'eeg': [
                np.sin(2 * np.pi * i * 10 * self.cycle * _time)
                for i in range(16)
            ],
        }


def _main():
    app = QtWidgets.QApplication([])
    window = SampleViewer(parent=None)
    window.show()
    thread = SampleAcquisitionThread(_BoardMock())
    thread.acquired.connect(window.append)
    thread.start()
    app.exec_()


if __name__ == '__main__':
    _main()
