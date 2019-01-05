import os

import umsgpack
import numpy as np
from PyQt5 import QtCore, QtWidgets

from bci_learning_studio.qt import qt_util
from .editor_ui import Ui_Editor


def _ask_open_path(parent):
    options = QtWidgets.QFileDialog.Options(
        QtWidgets.QFileDialog.DontUseNativeDialog
    )
    default_dir = qt_util.get_settings('default_load_dir')
    filename, _ = QtWidgets.QFileDialog.getOpenFileName(
        parent, 'Select recording to edit', default_dir, 'JSON (*.json)',
        options=options)
    if filename:
        qt_util.store_settings(default_load_dir=os.path.dirname(filename))
    return filename


def _load_file(path):
    with open(path, 'br') as fileobj:
        while True:
            try:
                yield umsgpack.load(fileobj)
            except umsgpack.InsufficientDataException:
                break


def _parse_data(path):
    eeg_data = {
        'sample_rate': None,
        'timestamps': [],
        'samples': [],
    }
    cursor_data = []
    target_data = {
        'timestamps': [],
        'coords': [],
    }
    for datum in _load_file(path):
        if datum['type'] == 'eeg':
            eeg_data['sample_rate'] = datum['data']['sampling_rate']
            eeg_data['timestamps'].append(datum['data']['timestamp'])
            eeg_data['samples'].append(datum['data']['eeg'])
        elif datum['type'] == 'cursor':
            cursor_data.append(datum['data'])
        else:
            target_data['timestamps'].append(datum['data']['time'])
            target_data['coords'].append(
                [datum['data']['x'], datum['data']['y']])
    eeg_data['timestamps'] = np.asarray(eeg_data['timestamps'])
    eeg_data['samples'] = np.asarray(eeg_data['samples']).T
    target_data['timestamps'] = np.asarray(target_data['timestamps'])
    target_data['coords'] = np.asarray(target_data['coords'])
    return {'eeg': eeg_data, 'cursor': cursor_data, 'target': target_data}


class Editor(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)

        self.ui = Ui_Editor()
        self.ui.setupUi(self)

        self.ui.actionOpen.triggered.connect(self._open_file)

        qt_util.restore_window_position(self)

        self._filename = None
        self._data = None
        self._bar = None

    ###########################################################################
    # Misc
    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        qt_util.store_window_position(self)
        if self.parent():
            self.parent().show()
        event.accept()

    def _center_replay(self):
        this_w = self.frameGeometry().width()
        geo = self.ui.cursorReplay.frameGeometry()
        rep_w, rep_h = geo.width(), geo.height()
        diff = (this_w - geo.width()) // 2
        self.ui.cursorReplay.setGeometry(diff, 0, rep_w, rep_h)
        self.update()
        geo = self.ui.cursorReplay.frameGeometry()

    ###########################################################################
    def _open_file(self, _):
        self._filename = _ask_open_path(self)
        if self._filename:
            self._load_file(self._filename)

    def _load_file(self, path):
        self._data = _parse_data(path)
        self._plot()

    def _plot(self):
        self.ui.viewer.plot(self._data['eeg'], self._data['target'])
        self.ui.viewer.seek_bar_dragged.connect(self._update_replay)

        self.ui.cursorReplay.set_cursor(x=0, y=1)
        self.ui.cursorReplay.set_target(x=0, y=0.5)
        self.ui.cursorReplay.update()

    ##########################################################################
    def _update_replay(self, timestamp):
        cursor = self._get_cursor_data(timestamp)
        if cursor:
            self.ui.cursorReplay.set_cursor(x=cursor['x'], y=cursor['y'])
            self.ui.cursorReplay.set_target(
                x=cursor['target_x'], y=cursor['target_y'])
            self.ui.cursorReplay.update()

    def _get_cursor_data(self, timestamp):
        ret = self._data['cursor'][0]
        for datum in self._data['cursor']:
            if datum['time'] > timestamp:
                break
            ret = datum
        return ret
