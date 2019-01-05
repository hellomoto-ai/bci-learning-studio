import os
import logging
import datetime

from PyQt5 import QtCore, QtWidgets

from bci_learning_studio.qt import qt_util
from bci_learning_studio.qt.device_manager import DeviceManager
from bci_learning_studio.qt.sample_serialization import SampleSerialization
from .recorder_ui import Ui_Recorder

_LG = logging.getLogger(__name__)


def _ask_save_path(parent):
    default_path = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S.json')
    default_dir = qt_util.get_settings('default_save_dir')
    if default_dir:
        default_path = os.path.join(default_dir, default_path)

    options = QtWidgets.QFileDialog.Options(
        QtWidgets.QFileDialog.DontConfirmOverwrite |
        QtWidgets.QFileDialog.DontUseNativeDialog
    )
    filename, _ = QtWidgets.QFileDialog.getSaveFileName(
        parent, 'Select recording path', default_path, 'JSON (*.json)',
        options=options)

    if filename:
        qt_util.store_settings(default_save_dir=os.path.dirname(filename))
    return filename


class Recorder(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)

        self.ui = Ui_Recorder()
        self.ui.setupUi(self)

        self.ui.actionDevice.triggered.connect(self._show_device_manager)
        self.ui.actionRecord.triggered.connect(self._toggle_recording)
        self.ui.actionStart.triggered.connect(self._toggle_interaction)
        self.ui.cursorControl.stopped.connect(self._stop_interaction)

        self._device_manager = DeviceManager(parent=self)
        self._serializer = None
        qt_util.restore_window_position(self)

    ###########################################################################
    # Misc
    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        qt_util.store_window_position(self)
        self._device_manager.disconnect()
        self.ui.cursorControl.stop()
        if self._serializer:
            self._terminate_serializer()
        if self.parent():
            self.parent().show()
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

    ###########################################################################
    # Recording / serialize
    def _init_serializer(self, filename):
        self._serializer = SampleSerialization(filename)
        self.ui.cursorControl.acquired.connect(self._serializer.save)
        self._device_manager.acquired.connect(self._serializer.save)

    def _terminate_serializer(self):
        self.ui.cursorControl.acquired.disconnect(self._serializer.save)
        self._device_manager.acquired.disconnect(self._serializer.save)
        self._serializer.close()
        self._serializer = None

    def _toggle_recording(self, checked):
        if checked:
            filename = _ask_save_path(self)
            if filename:
                self._init_serializer(filename)
            else:
                self.ui.actionRecord.setChecked(False)
        else:
            self._terminate_serializer()
