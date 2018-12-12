from collections import namedtuple

from PyQt5 import QtWidgets

from bci_learning_studio.qt.device_manager import device_manager

from . import conftest

# pylint: disable=protected-access


def _get_manager(qtbot):
    manager = device_manager.DeviceManager(parent=None)
    manager.show()
    qtbot.addWidget(manager)
    return manager


def test_inintial_menu_values(qtbot):
    """Only Connect and Plot actions are available"""
    manager = _get_manager(qtbot)

    assert manager.ui.actionConnect.isEnabled()
    assert not manager.ui.actionConnect.isChecked()
    assert manager.ui.actionConnect.text() == 'Connect'

    assert manager.ui.actionPlot.isEnabled()
    assert not manager.ui.actionPlot.isChecked()
    assert manager.ui.actionPlot.text() == 'Plot'

    assert not manager.ui.actionStream.isEnabled()
    assert not manager.ui.actionStream.isChecked()
    assert manager.ui.actionStream.text() == 'Stream'

    assert not manager.ui.actionConfigure.isEnabled()
    assert not manager.ui.actionConfigure.isChecked()
    assert manager.ui.actionConfigure.text() == 'Configure'


def test_connect_not_select(qtbot):
    """actionConnect is not checked when device selector rejects"""
    manager = _get_manager(qtbot)

    assert manager._selector is None
    assert not manager.ui.actionConnect.isChecked()
    manager.ui.actionConnect.activate(QtWidgets.QAction.Trigger)
    assert manager.ui.actionConnect.isChecked()
    assert manager._selector is not None
    manager._selector.reject()
    assert not manager.ui.actionConnect.isChecked()
    assert manager._selector is None


def test_connect_select_fail(qtbot, mocker):
    """Device selector is shown again if manager fails to connect the device"""
    def _connect(device):
        raise RuntimeError('Failed to connect device; %s' % device)

    mocker.patch.object(device_manager, '_connect', _connect)
    manager = _get_manager(qtbot)

    manager.ui.actionConnect.activate(QtWidgets.QAction.Trigger)
    manager._selector.selected.emit('foo')
    assert manager._selector.isVisible()


def test_connect_select_success(qtbot, mocker):
    """Device selector is closed if manager successfully connects the device"""
    def _connect(device):
        return namedtuple('Board', ['board_info'])(device)

    mocker.patch.object(device_manager, '_connect', _connect)
    manager = _get_manager(qtbot)

    manager.ui.actionConnect.activate(QtWidgets.QAction.Trigger)
    selector = manager._selector
    selector.selected.emit('foo')
    assert manager._selector is None
    assert not selector.isVisible()

    assert manager.ui.actionConnect.isEnabled()
    assert manager.ui.actionConnect.isChecked()
    assert manager.ui.actionConnect.text() == 'Disconnect'

    assert manager.ui.actionStream.isEnabled()
    assert not manager.ui.actionStream.isChecked()
    assert manager.ui.actionStream.text() == 'Stream'

    assert manager.ui.actionConfigure.isEnabled()
    assert not manager.ui.actionConfigure.isChecked()


def test_disconnect(qtbot, mocker):
    """Disconnect sets Connect/Stream/Configure state correctly."""
    def _connect(device):
        mock = namedtuple('Board', ['board_info', 'streaming', 'terminate'])
        return mock(device, False, lambda: 0)

    mocker.patch.object(device_manager, '_connect', _connect)
    manager = _get_manager(qtbot)

    manager.ui.actionConnect.activate(QtWidgets.QAction.Trigger)
    manager._selector.selected.emit('foo')
    manager.ui.actionConnect.activate(QtWidgets.QAction.Trigger)

    assert manager.ui.actionConnect.isEnabled()
    assert not manager.ui.actionConnect.isChecked()
    assert manager.ui.actionConnect.text() == 'Connect'

    assert not manager.ui.actionStream.isEnabled()
    assert not manager.ui.actionStream.isChecked()
    assert manager.ui.actionStream.text() == 'Stream'

    assert not manager.ui.actionConfigure.isEnabled()
    assert not manager.ui.actionConfigure.isChecked()
    assert manager.ui.actionConfigure.text() == 'Configure'


def test_configure(qtbot, mocker):
    """Disconnect sets Connect/Stream/Configure state correctly."""
    class Cyton:
        num_eeg = 16
        board_info = '''OpenBCI V3 8-16 channel
On Board ADS1299 Device ID: 0x3E
On Daisy ADS1299 Device ID: 0x3E
LIS3DH Device ID: 0x33
Firmware: v3.1.1
$$$'''
        def get_config(self):
            return conftest.get_default_channel_configs(self.num_eeg)

    def _connect(device):
        if device == 'Cyton':
            return Cyton()

    mocker.patch.object(device_manager, '_connect', _connect)
    manager = _get_manager(qtbot)

    manager.ui.actionConnect.activate(QtWidgets.QAction.Trigger)
    manager._selector.selected.emit('Cyton')
    manager.ui.actionConfigure.activate(QtWidgets.QAction.Trigger)
