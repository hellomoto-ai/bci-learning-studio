from PyQt5 import QtWidgets, QtCore

from .mode_selector_ui import Ui_ModeSelector
from .recorder import Recorder
from .editor import Editor


class ModeSelector(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)

        self.ui = Ui_ModeSelector()
        self.ui.setupUi(self)

        self.ui.actionRecord.triggered.connect(self._launch_record)
        self.ui.actionEdit.triggered.connect(self._launch_editor)

    def _launch_record(self, _):
        recorder = Recorder(parent=self)
        recorder.show()
        recorder.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.hide()

    def _launch_editor(self, _):
        editor = Editor(parent=self)
        editor.show()
        editor.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.hide()

    ###########################################################################
    # Misc
    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Escape:
            self.close()
