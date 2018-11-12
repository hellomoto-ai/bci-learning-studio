import os
import json
import logging
import datetime

from PyQt5 import QtCore, QtWidgets

from bci_learning_studio.qt import qt_util
from bci_learning_studio.qt.device_manager import DeviceManager
from .main_window_ui import Ui_MainWindow

_LG = logging.getLogger(__name__)


def _ask_save_path():
    default_path = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S.json')
    default_dir = qt_util.get_settings('default_save_path')
    if default_dir:
        default_path = os.path.join(default_dir, default_path)

    options = QtWidgets.QFileDialog.Options(
        QtWidgets.QFileDialog.DontConfirmOverwrite |
        QtWidgets.QFileDialog.DontUseNativeDialog
    )
    filename, _ = QtWidgets.QFileDialog.getSaveFileName(
        None, 'Select recording path', default_path, 'JSON (*.json)',
        options=options)

    qt_util.store_settings(default_save_path=os.path.dirname(filename))
    return filename


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionDevice.triggered.connect(self._show_device_manager)
        self.ui.actionRecord.triggered.connect(self._toggle_recording)
        self.ui.actionStart.triggered.connect(self._toggle_interaction)
        self.ui.cursorControl.stopped.connect(self._stop_interaction)
        self.ui.cursorControl.acquired.connect(self._store_cursor)

        self._device_manager = DeviceManager(parent=self)

        self._buffer = []
        self._recording = False
        self._save_path = None

        qt_util.restore_window_position(self)

    ###########################################################################
    # Misc
    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        self._device_manager.disconnect()
        self.ui.cursorControl.stop()
        qt_util.store_window_position(self)
        event.accept()

    ###########################################################################
    # Device Manager
    def _show_device_manager(self):
        # To bring to front, hide once
        self._device_manager.hide()
        self._device_manager.show()

    ###########################################################################
    # Interactive session
    def _toggle_interaction(self, checked):
        if checked:
            self._stop_interaction()
        else:
            self._start_interaction()

    def _start_interaction(self):
        self.ui.cursorControl.start()
        self.ui.actionStart.setChecked(True)
        self.ui.actionStart.setText('Stop')

    def _stop_interaction(self):
        self.ui.cursorControl.stop()
        self.ui.actionStart.setChecked(False)
        self.ui.actionStart.setText('Start')
        if self._recording:
            self._save()

    def _store_cursor(self, value):
        self._buffer.append(value)

    ###########################################################################
    # Recording / save
    def _toggle_recording(self, checked):
        if checked:
            self._start_recording()
        else:
            self._stop_recording()

    def _start_recording(self):
        filename = _ask_save_path()
        if not filename:  # user canneled.
            self.ui.actionRecord.setChecked(False)
            return
        self._recording = True
        self._save_path = filename

    def _stop_recording(self):
        self._recording = False
        self._save_path = None

    def _save(self):
        _LG.info('Saving data %s', self._save_path)
        with open(self._save_path, 'a') as fileobj:
            for data in self._buffer:
                json.dump(data, fileobj)
                fileobj.write('\n')
