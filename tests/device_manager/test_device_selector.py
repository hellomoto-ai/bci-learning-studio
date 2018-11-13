from collections import namedtuple

from PyQt5 import QtCore
from bci_learning_studio.qt.device_manager import device_selector


def _get_comports(vals):
    port = namedtuple('Port', ['device'])

    def _comports():
        return [port(val) for val in vals]
    return _comports


def test_device_selector(qtbot, mocker):
    """DeviceSelector emits `selected` signal if a valid device is selected."""
    port_names = ['foo', 'bar', 'baz']

    _comports = _get_comports(port_names)
    mocker.patch.object(
        device_selector.serial.tools.list_ports, 'comports', _comports)
    selector = device_selector.DeviceSelector(parent=None)
    selector.show()
    qtbot.addWidget(selector)

    device_list = selector.ui.deviceList
    for name in port_names:
        with qtbot.waitSignal(selector.selected, timeout=1000) as blocker:
            device_list.setCurrentIndex(device_list.findText(name))
            qtbot.mouseClick(selector.ui.connectButton, QtCore.Qt.LeftButton)
        assert blocker.args == [name]
        assert QtCore.QSettings().value('last_used_device') == name

    with qtbot.assertNotEmitted(selector.selected):
        device_list.setCurrentIndex(device_list.findText('boo'))
        qtbot.mouseClick(selector.ui.connectButton, QtCore.Qt.LeftButton)
