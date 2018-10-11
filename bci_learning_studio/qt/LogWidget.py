import logging
import datetime

from PyQt5 import QtGui, QtWidgets

from bci_learning_studio import __version__
from .LogWidget_Ui import Ui_LogWidget

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


class _TextWidgetHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()

        self.buffer = []
        self.text_widget = text_widget

    def emit(self, record):
        self.buffer.append(record)
        self.text_widget.setTextColor(_get_color(record.levelno))
        # In normal logging mechanism comparing levels are not necessary as
        # it is already handled.
        # But for re-showing past logs with filter applied
        # (as in `refresh` method), it is necessary to re-compare log level.
        if record.levelno >= self.level:
            self.text_widget.append(self.format(record))

    def clear(self):
        """Clear displayed logs and log buffers in this class"""
        self.buffer = []
        self.text_widget.clear()

    def refresh(self):
        """Re-show log records."""
        records = self.buffer
        self.clear()
        for record in records:
            self.emit(record)

    def get_unfiltered_logs(self):
        """Get unfiltered log texts."""
        for record in self.buffer:
            yield self.format(record)


def _get_handler(text_widget):
    format_ = '%(asctime)s: %(levelname)8s: %(message)s'
    handler = _TextWidgetHandler(text_widget)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(format_))
    logging.getLogger().addHandler(handler)
    return handler


class LogWidget(QtGui.QWidget, Ui_LogWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.pushButtonClear.pushed.connect(self._clear)
        self.pushButtonSave.pushed.conenct(self._save)
        self.comboBoxFilter.addItems([
            'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL',
        ])
        self.comboBoxFilter.currentIndexChanged.connect(self._filter)

        self._handler = _get_handler(self.textEditLog)

    def _set_status(self, message):
        self.window().statusBar().showMessage(message)

    def _clear(self):
        self._handler.clear()

    def _filter(self):
        level = self.comboBoxFilter.currentText()
        self._handler.setLevel(level)
        self._handler.refresh()

    def _save(self):
        filename = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S.txt')

        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save log to file', filename,
            'All Files (*);;Text Files (*.txt)',
            options=options)

        with open(filename, 'w') as fileobj:
            fileobj.write('BCI Learning Studio: %s\n' % __version__)
            for line in self._handler.get_unfiltered_logs():
                fileobj.write(line)
                fileobj.write('\n')
        self._set_status('Log saved; %s' % filename)
