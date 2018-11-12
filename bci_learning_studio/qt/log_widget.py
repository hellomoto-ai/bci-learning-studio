import logging
import datetime

from PyQt5 import QtWidgets, QtGui, QtCore

from .log_widget_ui import Ui_LogWidget

_LG = logging.getLogger(__name__)

_RED = QtGui.QColor(255, 5, 5)
_ORANGE = QtGui.QColor(242, 169, 60)
_BRACK = QtGui.QColor(0, 0, 0)
_BROWN = QtGui.QColor(90, 30, 30)


def _get_color(levelno):
    if levelno >= logging.ERROR:
        return _RED
    if levelno >= logging.WARNING:
        return _ORANGE
    if levelno >= logging.INFO:
        return _BRACK
    return _BROWN


def _add_handler(handler):
    format_ = '%(asctime)s: %(levelname)8s: %(message)s'
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(format_))
    logging.getLogger().addHandler(handler)
    return handler


class _Widget(QtWidgets.QWidget):
    acquired = QtCore.pyqtSignal('PyQt_PyObject')


class SignalHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self._widget = _Widget()
        self.acquired = self._widget.acquired

    def emit(self, record):
        text = self.format(record)
        level = record.levelno
        self._widget.acquired.emit((level, text))


class LogWidget(QtWidgets.QWidget, logging.Handler):
    def __init__(self, parent=None):
        super(QtWidgets.QWidget, self).__init__(parent)

        self.ui = Ui_LogWidget()
        self.ui.setupUi(self)

        self._handler = SignalHandler()
        self._handler.acquired.connect(self._add_record)
        _add_handler(self._handler)

        self._buffer = []
        self._setup_ui()
        self._levelno = self.ui.levelBox.currentData()

    def _setup_ui(self):
        self.ui.clearButton.clicked.connect(self._clear)
        self.ui.saveButton.clicked.connect(self._save_log)
        self.ui.levelBox.clear()
        for level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            levelno = getattr(logging, level)
            self.ui.levelBox.addItem(level, levelno)
        self.ui.levelBox.setCurrentIndex(self.ui.levelBox.findText('INFO'))
        self.ui.levelBox.currentIndexChanged.connect(self._change_level)

    def _change_level(self, _):
        self._levelno = self.ui.levelBox.currentData()
        self.ui.textEdit.clear()
        for record in self._buffer:
            self._add_text(record)
        self._move_bar()

    def _add_record(self, record):
        self._buffer.append(record)
        self._add_text(record)
        self._move_bar()

    def _add_text(self, record):
        level, text = record
        self.ui.textEdit.setTextColor(_get_color(level))
        if level >= self._levelno:
            self.ui.textEdit.append(text)

    def _move_bar(self):
        bar_ = self.ui.textEdit.verticalScrollBar()
        max_val = bar_.maximum()
        if max_val - bar_.value() < 2:
            bar_.setValue(max_val)

    def _clear(self):
        self._buffer = []
        self.ui.textEdit.clear()

    def _save_log(self):
        filename = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S.log')

        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save log', filename, 'Log Files (*.log)',
            options=QtWidgets.QFileDialog.Options())

        if not filename:
            return

        with open(filename, 'w') as fileobj:
            for _, text in self._buffer:
                fileobj.write(text)
                fileobj.write('\n')
