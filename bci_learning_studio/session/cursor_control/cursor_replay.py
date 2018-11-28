from PyQt5 import QtWidgets, QtGui, QtCore

from .cursors import CursorManager


class CursorReplay(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setAttribute(QtCore.Qt.WA_StyledBackground)

        self._manager = CursorManager()

    def set_cursor(self, x, y):
        self._manager.cursor.x = x
        self._manager.cursor.y = y

    def set_target(self, x, y):
        self._manager.target.x = x
        self._manager.target.y = y

    ###########################################################################
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        self._manager.draw(painter, self.frameGeometry())
