import json
import datetime

from PyQt5 import QtCore, QtWidgets

from bci_learning_studio.qt import qt_util
from bci_learning_studio.qt.device_manager import DeviceManager
from .main_window_ui import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionStart.triggered.connect(self._toggle)
        self.ui.actionSave.triggered.connect(self._save)
        self.ui.actionDevice.triggered.connect(self._show_device_manager)
        self.ui.cursorControl.stopped.connect(self._stop)
        self.ui.cursorControl.acquired.connect(self._store_cursor)

        self._device_manager = DeviceManager(parent=self)

        self._buffer = []

        qt_util.restore_window_position(self)

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        self._device_manager.disconnect()
        self.ui.cursorControl.stop()
        qt_util.store_window_position(self)
        event.accept()

    def _toggle(self, checked):
        if checked:
            self._start()
        else:
            self._stop()

    def _start(self):
        self.ui.cursorControl.start()
        self.ui.actionStart.setChecked(True)
        self.ui.actionStart.setText('Stop')

    def _stop(self):
        self.ui.cursorControl.stop()
        self.ui.actionStart.setChecked(False)
        self.ui.actionStart.setText('Start')

    def _store_cursor(self, value):
        self._buffer.append(value)

    def _save(self):
        filename = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S.json')

        options = QtWidgets.QFileDialog.Options()
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save recording to file', filename, 'JSON Files (*.json)',
            options=options)

        if not filename:
            return

        with open(filename, 'w') as fileobj:
            for data in self._buffer:
                json.dump(data, fileobj)
                fileobj.write('\n')

    def _show_device_manager(self):
        # To bring to front, hide once
        self._device_manager.hide()
        self._device_manager.show()
