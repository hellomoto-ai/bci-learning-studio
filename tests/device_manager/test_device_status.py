from bci_learning_studio.qt.device_manager import (
    device_status,
    measurement_status_indicator,
)

# pylint: disable=protected-access


def test_device_status(qtbot):
    """Test DeiveStatus module"""
    status = device_status.DeviceStatus(parent=None)
    status.show()
    qtbot.addWidget(status)

    # Test initial value
    board_info = 'test board info'
    status.init(board_info)

    assert status.ui.boardInfo.toPlainText() == board_info
    assert status.ui.sampleRate.text() == '0.00'

    # Test updated values
    timestamp = 0.0
    for sample_rate in [250, 500, 1000, 8000, 16000]:
        diff = 1 / sample_rate
        for _ in range(5000):
            sample = {
                'type': 'eeg',
                'data': {
                    'timestamp': timestamp,
                    'raw_eeg': [],
                },
            }
            status.tick(sample)
            timestamp += diff
        assert status.ui.sampleRate.text() == '%.2f' % sample_rate

    # Test indicator
    indicator = status.ui.measurementStatusIndicator
    railed = int(pow(2, 23))
    for val in [railed, railed - 999]:
        raw_eeg = [0] * 16
        for sign in [1, -1]:
            raw_eeg[0] = sign * val
            sample = {
                'type': 'eeg',
                'data': {
                    'timestamp': 0,
                    'raw_eeg': raw_eeg,
                },
            }
            status.tick(sample)
            assert indicator._status == measurement_status_indicator._RAILED

    for val in [railed-1001, int(railed * 0.9) + 1]:
        raw_eeg = [0] * 16
        for sign in [1, -1]:
            raw_eeg[0] = sign * val
            sample = {
                'type': 'eeg',
                'data': {
                    'timestamp': 0,
                    'raw_eeg': raw_eeg,
                },
            }
            status.tick(sample)
            assert indicator._status == measurement_status_indicator._NEAR_RAILED

    for val in [1, int(railed * 0.9) - 1]:
        raw_eeg = [0] * 16
        for sign in [1, -1]:
            raw_eeg[0] = sign * val
            sample = {
                'type': 'eeg',
                'data': {
                    'timestamp': 0,
                    'raw_eeg': raw_eeg,
                },
            }
            status.tick(sample)
            assert indicator._status == measurement_status_indicator._OK

