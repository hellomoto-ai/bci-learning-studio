from PyQt5 import QtCore


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
