from PyQt5 import QtCore, QtGui, QtWidgets

import openbci_interface
from .cyton_configuration_ui import Ui_CytonConfiguration


def _init_table(table, num_channels):
    table.setRowCount(num_channels)
    table.setColumnCount(7)

    for row in range(num_channels):
        box = QtWidgets.QCheckBox()
        box.setChecked(True)
        box.setStyleSheet('margin-left:50%; margin-right:50%;')
        table.setCellWidget(row, 0, box)

        box = QtWidgets.QComboBox()
        for val in ['ON', 'OFF']:
            box.addItem(val, val)
        box.setCurrentIndex(box.findData('OFF'))
        table.setCellWidget(row, 1, box)

        box = QtWidgets.QComboBox()
        for val in [1, 2, 4, 6, 8, 12, 24]:
            box.addItem(str(val), val)
        box.setCurrentIndex(box.findData(24))
        table.setCellWidget(row, 2, box)

        vals = [
            'NORMAL', 'SHORTED', 'BIAS_MEAS', 'MVDD',
            'TEMP', 'TESTSIG', 'BIAS_DRP', 'BIAS_DRN',
        ]
        box = QtWidgets.QComboBox()
        for val in vals:
            box.addItem(val, val)
        box.setCurrentIndex(box.findData('NORMAL'))
        table.setCellWidget(row, 3, box)

        box = QtWidgets.QComboBox()
        for val in [0, 1]:
            box.addItem(str(val), val)
        box.setCurrentIndex(box.findData(1))
        table.setCellWidget(row, 4, box)

        box = QtWidgets.QComboBox()
        for val in [0, 1]:
            box.addItem(str(val), val)
        box.setCurrentIndex(box.findData(1))
        table.setCellWidget(row, 5, box)

        box = QtWidgets.QComboBox()
        for val in [0, 1]:
            box.addItem(str(val), val)
        box.setCurrentIndex(box.findData(0))
        table.setCellWidget(row, 6, box)

    headers = [
        'Enabled', 'Power Down', 'Gain',
        'Input Type', 'Bias', 'SRB2', 'SRB1']
    for col, val in enumerate(headers):
        header = QtWidgets.QTableWidgetItem(val)
        table.setHorizontalHeaderItem(col, header)


class CytonConfig(QtWidgets.QMainWindow):
    applied = QtCore.pyqtSignal('PyQt_PyObject')

    def __init__(self, parent, num_channels):
        super().__init__(parent=parent)

        self.ui = Ui_CytonConfiguration()
        self.ui.setupUi(self)
        self.num_channels = num_channels

        self._init_ui()

        btn = self.ui.buttonBox.button(QtGui.QDialogButtonBox.Apply)
        btn.clicked.connect(self._apply_clicked)

    def _init_ui(self):
        self._init_board_config_ui()
        self._init_channel_config_ui()

    def _init_board_config_ui(self):
        box = self.ui.boardMode_ComboBox
        box.clear()
        for val in ['default', 'debug', 'analog', 'digital', 'marker']:
            box.addItem(val.capitalize(), val)
        box.setCurrentIndex(box.findData('default'))

        box = self.ui.sampleRate_ComboBox
        box.clear()
        for val in [250, 500, 1000, 2000, 4000, 8000, 16000]:
            box.addItem(str(val), val)
        box.setCurrentIndex(box.findData(250))

    def _init_channel_config_ui(self):
        _init_table(self.ui.channelConfig_Table, self.num_channels)

    def _get_configs(self):
        widget = self.ui.channelConfig_Table.cellWidget
        return {
            'board_mode': self.ui.boardMode_ComboBox.currentData(),
            'sample_rate': self.ui.sampleRate_ComboBox.currentData(),
            'channels': [{
                'enabled': widget(row, 0).isChecked(),
                'parameters': {
                    'power_down': widget(row, 1).currentData(),
                    'gain': widget(row, 2).currentData(),
                    'input_type': widget(row, 3).currentData(),
                    'bias': widget(row, 4).currentData(),
                    'srb2': widget(row, 5).currentData(),
                    'srb1': widget(row, 6).currentData(),
                },
            } for row in range(self.num_channels)]
        }

    def set_config(self, config):
        box = self.ui.boardMode_ComboBox
        box.setCurrentIndex(box.findData(config['board_mode']))
        box = self.ui.sampleRate_ComboBox
        box.setCurrentIndex(box.findData(config['sample_rate']))

        widget = self.ui.channelConfig_Table.cellWidget
        keys = [
            'power_down', 'gain', 'input_type', 'bias', 'srb2', 'srb1'
        ]
        for row, cfg in enumerate(config['channels']):
            widget(row, 0).setChecked(cfg['enabled'])
            for col, key in enumerate(keys, start=1):
                box = widget(row, col)
                index = box.findData(cfg['parameters'][key])
                if index >= 0:
                    box.setCurrentIndex(index)

    def _apply_clicked(self):
        self.statusBar().showMessage('Applying configurations ...')
        self.applied.emit(self._get_configs())


def get_config_dialog(board, parent):
    if isinstance(board, openbci_interface.Cyton):
        return CytonConfig(parent, num_channels=board.num_eeg)
    raise NotImplementedError(
        'Not supported; %s' % board.__class__.__name__)
