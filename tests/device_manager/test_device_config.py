from PyQt5 import QtCore
from bci_learning_studio.qt.device_manager import device_config


def _get_default_values(num_channels):
    return {
        'board_mode': 'default',
        'sample_rate': 250,
        'channels': [
            {
                'enabled': True,
                'parameters': {
                    'power_down': 'OFF',
                    'gain': 24, 'input_type': 'NORMAL',
                    'bias': 1, 'srb2': 1, 'srb1': 0,
                },
            }
        ] * num_channels
    }


def test_cyton_config(qtbot):
    """Test CytonConfiguration class"""
    num_channels = 16
    cyton_config = device_config.CytonConfig(
        parent=None, num_channels=num_channels)
    cyton_config.show()
    qtbot.addWidget(cyton_config)

    # Check Default values
    assert cyton_config.ui.boardMode_ComboBox.currentText() == 'Default'
    assert cyton_config.ui.boardMode_ComboBox.currentData() == 'default'
    assert cyton_config.ui.sampleRate_ComboBox.currentText() == '250'
    assert cyton_config.ui.sampleRate_ComboBox.currentData() == 250

    table = cyton_config.ui.channelConfig_Table
    headers = [
        'Enabled', 'Power Down', 'Gain',
        'Input Type', 'Bias', 'SRB2', 'SRB1']
    for i, header in enumerate(headers):
        assert table.horizontalHeaderItem(i).text() == header

    cells = table.cellWidget
    for row in range(num_channels):
        assert cells(row, 0).isChecked()
        assert cells(row, 1).currentText() == 'OFF'
        assert cells(row, 1).currentData() == 'OFF'
        assert cells(row, 2).currentText() == '24'
        assert cells(row, 2).currentData() == 24
        assert cells(row, 3).currentText() == 'NORMAL'
        assert cells(row, 3).currentData() == 'NORMAL'
        assert cells(row, 4).currentText() == '1'
        assert cells(row, 4).currentData() == 1
        assert cells(row, 5).currentText() == '1'
        assert cells(row, 5).currentData() == 1
        assert cells(row, 6).currentText() == '0'
        assert cells(row, 6).currentData() == 0

    # Check emitted values
    default_data = _get_default_values(num_channels)
    with qtbot.waitSignal(cyton_config.applied, timeout=1000) as blocker:
        apply_button = cyton_config.ui.buttonBox.buttons()[0]
        qtbot.mouseClick(apply_button, QtCore.Qt.LeftButton)
    assert blocker.args == [default_data]
