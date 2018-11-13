import time
import logging

import openbci_interface
import serial as pyserial
from PyQt5 import QtCore, QtWidgets

from bci_learning_studio.qt import qt_util
from .device_manager_ui import Ui_DeviceManager
from .device_selector import DeviceSelector
from . import device_config
from .sample_acquisition import SampleAcquisitionThread
from .sample_plotter import SamplePlotter

_LG = logging.getLogger(__name__)


def _user_confirms(parent, title, message):
    result = QtWidgets.QMessageBox.question(
        parent, title, message,
        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
    )
    return result == QtWidgets.QMessageBox.Yes


def _connect(device):
    try:
        ser = pyserial.Serial(port=device, baudrate=115200, timeout=3)
    except Exception:  # pylint: disable=broad-except
        err_msg = 'Failed to open serial connection; %s' % device
        raise RuntimeError(err_msg) from None

    try:
        ser.write(b'v')
        message = ser.read_until(b'$$$').decode('utf-8', errors='ignore')
    except Exception:  # pylint: disable=broad-except
        ser.close()
        err_msg = 'Failed to fetch board info from %s' % device
        raise RuntimeError(err_msg) from None

    if not message.endswith('$$$'):
        err_msg = 'Failed to fetch board info.'
        raise RuntimeError(err_msg) from None

    if 'ADS1299' in message:
        board = openbci_interface.Cyton(ser, close_on_terminate=True)
        board.initialize()
        return board

    raise RuntimeError('Unexpected board. %s' % message)


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
        self._selector = None

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
        self.ui.deviceStatus.init(self._board.board_info)

    def _set_ui_disconnected(self):
        self.ui.actionConnect.setChecked(False)
        self.ui.actionConnect.setText('Connect')
        self.ui.actionStream.setEnabled(False)
        self.ui.actionStream.setChecked(False)
        self.ui.actionStream.setText('Stream')
        self.ui.actionConfigure.setEnabled(False)

    def _toggle_connect(self, checked):
        if checked:
            self._launch_selector()
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

    def _launch_selector(self):
        self._selector = DeviceSelector(parent=self)
        self._selector.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self._selector.selected.connect(self._connect_board)
        self._selector.show()

    def _connect_board(self, device):
        self._selector.hide()
        self._show_message('Connecting %s' % device)
        try:
            self._board = _connect(device)
        except Exception as error:  # pylint: disable=broad-except
            self._show_message(str(error))
            _LG.exception('Failed to initialize device; %s', device)
            self._selector.show()
            return
        self._show_message('Connected %s' % device)
        self._selector.close()
        self._set_ui_connected()

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
        self._board_config = device_config.get_config_dialog(self._board, self)
        self._board_config.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self._board_config.set_configs(self._board)
        self._board_config.applied.connect(self._configure_board)
        self._board_config.show()

    def _configure_board(self, configs):
        self._board_config.setEnabled(False)
        self._set_channel_configs(configs['channel'])
        self._set_board_configs(configs['board'])
        self._board_config.set_configs(self._board)
        self._board_config.statusBar().showMessage('Configurations applied.')
        self._board_config.setEnabled(True)

    def _set_channel_configs(self, new_configs):
        current_configs = self._board_config.get_config(self._board)['channel']
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
        current_configs = self._board_config.get_config(self._board)['board']
        if current_configs['board_mode'] != configs['board_mode']:
            self._board.set_board_mode(configs['board_mode'])
            time.sleep(0.1)
        if current_configs['sample_rate'] != configs['sample_rate']:
            self._board.set_sample_rate(configs['sample_rate'])
            time.sleep(0.1)
