from bci_learning_studio.qt.device_manager import device_status


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
            sample = {'timestamp': timestamp}
            status.tick(sample)
            timestamp += diff
        assert status.ui.sampleRate.text() == '%.2f' % sample_rate
