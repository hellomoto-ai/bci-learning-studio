import time
import logging

import serial
import openbci_interface
from PyQt5 import QtCore, QtWidgets

from bci_learning_studio.qt import qt_util
from .device_manager_ui import Ui_DeviceManager
from .device_selector import DeviceSelector
from .device_config import get_config_dialog
from .sample_plotter import SamplePlotter

_LG = logging.getLogger(__name__)


class SampleAcquisitionThread(QtCore.QThread):
    acquired = QtCore.pyqtSignal('PyQt_PyObject')

    def __init__(self, board, wait_factor=0.85):
        super().__init__()
        self._board = board
        self.wait_factor = wait_factor

    def run(self):
        _LG.info('Starting sample acquisition thread.')

        # `cycle` here is a sensitive value;
        # Setting it same as (1.0 * board.cycle) will cause sample acquisition
        # out of sync (delayed) and you will see end byte not matching to
        # expected value -> wrong value.
        # Setting it to (0.5 * board.cycle) will cause sample acquisition
        # too quick so that sample distribution over time is skewed.
        #
        # 0.85 was found okay in the sense that it does not cause wrong
        # end byte while sample distribution over time is kind of smooth.
        cycle = self.wait_factor * self._board.cycle
        unit_wait = cycle / 10.0
        last_acquired = time.time()
        while self._board.streaming:
            now = time.time()
            if now - last_acquired < cycle:
                self.sleep(unit_wait)
                continue
            try:
                sample = self._board.read_sample()
                if sample['valid']:
                    self.acquired.emit(sample)
            except serial.serialutil.SerialException:
                _LG.info('Connection seems to be closed.')
            except Exception:  # pylint: disable=broad-except
                _LG.exception('failed to fetch')
            last_acquired = now
        _LG.info('Sample acquisition thread stopped.')


def _user_confirms(parent, title, message):
    result = QtWidgets.QMessageBox.question(
        parent, title, message,
        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
    )
    return result == QtWidgets.QMessageBox.Yes


def _get_config(board):
    return {
        'board': {
            'board_mode': board.board_mode,
            'sample_rate': board.sample_rate,
        },
        'channel': [
            {
                'enabled': config.enabled,
                'parameters': {
                    'power_down': config.power_down,
                    'gain': config.gain,
                    'input_type': config.input_type,
                    'bias': config.bias,
                    'srb2': config.srb2,
                    'srb1': config.srb1,
                },
            } for config in board.channel_configs
        ],
    }


class DeviceManager(QtWidgets.QMainWindow):
    connected = QtCore.pyqtSignal(bool)
    streaming = QtCore.pyqtSignal(bool)
    acquired = QtCore.pyqtSignal('PyQt_PyObject')

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)

        self.ui = Ui_DeviceManager()
        self.ui.setupUi(self)

        self.ui.actionConnect.triggered.connect(self._toggle_connect)
        self.ui.actionStream.triggered.connect(self._toggle_stream)
        self.ui.actionConfigure.triggered.connect(self._launch_config_dialog)
        self.ui.actionPlot.triggered.connect(self._show_sample_plotter)

        self._sample_plotter = SamplePlotter(parent=self)

        self._set_ui_disconnected()
        self._board = None
        self._sample_acquisition = None
        self._board_config = None

        qt_util.restore_window_position(self)

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        qt_util.store_window_position(self)
        event.accept()

    def _show_message(self, message):
        self.statusBar().showMessage(message)

    ###########################################################################
    # Connect / Disconnect functions
    def _set_ui_connected(self):
        self.ui.actionConnect.setChecked(True)
        self.ui.actionConnect.setText('Disconnect')
        self.ui.actionStream.setEnabled(True)
        self.ui.actionStream.setChecked(False)
        self.ui.actionStream.setText('Stream')
        self.ui.actionConfigure.setEnabled(True)
        self.ui.deviceStatus.set_sample_rate(0)
        self.ui.deviceStatus.set_board_info(self._board.board_info)

    def _set_ui_disconnected(self):
        self.ui.actionConnect.setChecked(False)
        self.ui.actionConnect.setText('Connect')
        self.ui.actionStream.setEnabled(False)
        self.ui.actionStream.setChecked(False)
        self.ui.actionStream.setText('Stream')
        self.ui.actionConfigure.setEnabled(False)

    def _toggle_connect(self, checked):
        if checked:
            self._launch_detector()
            self.ui.actionConnect.setChecked(False)
            self.connected.emit(True)
        else:
            if self._board.streaming:
                confirmed = _user_confirms(
                    self, 'Device Streaming',
                    'The device is streaming data. Proceed?',
                )
                if not confirmed:
                    self.ui.actionConnect.setChecked(True)
                    return
            self.disconnect()
            self.connected.emit(False)

    def _launch_detector(self):
        selector = DeviceSelector(parent=self)
        selector.message.connect(self._show_message)
        selector.detected.connect(self._connect)
        selector.show()

    def _connect(self, device, board_type):
        try:
            board_class = getattr(openbci_interface, board_type)
        except AttributeError:
            self._show_message('Unsupported board type: %s' % board_type)
            return
        self._initialize_board(device, board_class)
        self._set_ui_connected()

    def _initialize_board(self, port, board_class):
        self._show_message('Connecting %s' % port)
        ser = serial.Serial(port=port, baudrate=115200, timeout=2)
        self._board = board_class(ser, close_on_terminate=True)
        self._board.initialize()
        self._show_message('Connected %s(%s)' % (board_class.__name__, port))

    def disconnect(self):
        if self._board is not None:
            self._board.terminate()
            self._show_message('Disconnected.')
        if self._sample_acquisition is not None:
            self._sample_acquisition.wait()
            self._sample_acquisition = None
        self._sample_plotter.close()
        self._set_ui_disconnected()

    ###########################################################################
    # Stream / Stop functions
    def _toggle_stream(self, checked):
        if checked:
            self._start_streaming()
            self.streaming.emit(True)
        else:
            self._stop_streaming()
            self.streaming.emit(False)

    def _stop_streaming(self):
        self._board.stop_streaming()
        self._sample_acquisition.wait()
        self._sample_acquisition = None
        self._sample_plotter.reset()
        self.ui.actionStream.setText('Stream')

    def _start_streaming(self):
        self._sample_acquisition = SampleAcquisitionThread(self._board)
        self._sample_acquisition.acquired.connect(self.acquired.emit)
        self._sample_acquisition.acquired.connect(self.ui.deviceStatus.tick)
        self._sample_acquisition.acquired.connect(self._sample_plotter.append)
        self._board.start_streaming()
        self._sample_acquisition.start()
        self.ui.actionStream.setText('Stop')

    ###########################################################################
    # Plot window show/hide
    def _show_sample_plotter(self):
        # To bring to front, hide once
        self._sample_plotter.hide()
        self._sample_plotter.show()

    ###########################################################################
    # Configure board
    def _launch_config_dialog(self):
        config = get_config_dialog(type(self._board).__name__)
        self._board_config = config(
            parent=self, num_channels=self._board.num_eeg)
        self._board_config.set_configs(_get_config(self._board))
        self._board_config.applied.connect(self._configure_board)
        self._board_config.show()

    def _configure_board(self, configs):
        self._board_config.setEnabled(False)
        self._set_channel_configs(configs['channel'])
        self._set_board_configs(configs['board'])
        self._board_config.set_configs(_get_config(self._board))
        self._board_config.statusBar().showMessage('Configurations applied.')
        self._board_config.setEnabled(True)

    def _set_channel_configs(self, new_configs):
        current_configs = _get_config(self._board)['channel']
        generator = enumerate(zip(current_configs, new_configs), start=1)
        for channel, (current_cfg, new_cfg) in generator:
            enabled, params = new_cfg['enabled'], new_cfg['parameters']

            if current_cfg['enabled'] != enabled and enabled:
                self._board.enable_channel(channel)
                time.sleep(0.1)
            if current_cfg['parameters'] != params:
                self._board.configure_channel(channel=channel, **params)
                time.sleep(0.1)
            if current_cfg['enabled'] != enabled and not enabled:
                self._board.disable_channel(channel)
                time.sleep(0.1)

    def _set_board_configs(self, configs):
        if self._board.streaming:
            return
        current_configs = _get_config(self._board)['board']
        if current_configs['board_mode'] != configs['board_mode']:
            self._board.set_board_mode(configs['board_mode'])
            time.sleep(0.1)
        if current_configs['sample_rate'] != configs['sample_rate']:
            self._board.set_sample_rate(configs['sample_rate'])
            time.sleep(0.1)
