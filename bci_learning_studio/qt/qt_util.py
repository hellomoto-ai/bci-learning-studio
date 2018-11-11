from PyQt5 import QtCore, QtWidgets


class PeriodicCall(QtCore.QThread):
    elapsed = QtCore.pyqtSignal()

    def __init__(self, fps=30):
        super().__init__()
        self.fps = fps
        self._stop_requested = False

    def run(self):
        sleep_msec = int(1000 / self.fps)
        while not self._stop_requested:
            self.msleep(sleep_msec)
            self.elapsed.emit()
        self._stop_requested = False

    def stop(self):
        self._stop_requested = True


def store_window_position(window):
    name = window.objectName()
    settings = QtCore.QSettings()
    settings.setValue('%s/geometry' % name, window.saveGeometry())
    settings.setValue('%s/windowState' % name, window.saveState())


def restore_window_position(window):
    name = window.objectName()
    settings = QtCore.QSettings()
    val = settings.value('%s/geometry' % name)
    if val is not None:
        window.restoreGeometry(val)
    val = settings.value('%s/windowState' % name)
    if val is not None:
        window.restoreState(val)


def ask_save_path(parent, default_filename):
    filename, _ = QtWidgets.QFileDialog.getSaveFileName(
        parent, 'Save recording to file',
        default_filename,
        'JSON Files (*.json)',
        options=QtWidgets.QFileDialog.Options())
    return filename
