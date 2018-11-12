from PyQt5 import QtCore


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


def store_settings(**kwargs):
    settings = QtCore.QSettings()
    for key, value in kwargs.items():
        settings.setValue(key, value)


def get_settings(key, *other_keys):
    settings = QtCore.QSettings()
    if not other_keys:
        return settings.value(key)
    keys = [key] + other_keys
    return [settings.value(key) for key in keys]
