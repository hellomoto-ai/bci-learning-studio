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
    name = '%s/geometry' % window.objectName()
    store_settings(**{name: window.saveGeometry()})


def restore_window_position(window):
    name = '%s/geometry' % window.objectName()
    val = get_settings(name)
    if val is not None:
        window.restoreGeometry(val)


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
