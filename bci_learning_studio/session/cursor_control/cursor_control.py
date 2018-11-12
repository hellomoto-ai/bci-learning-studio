import time

from PyQt5 import QtWidgets, QtCore, QtGui

from .cursor_control_ui import Ui_CursorControl
from .cursors import Point2D, CursorManager


class CursorControl(QtWidgets.QWidget):
    acquired = QtCore.pyqtSignal(dict)
    stopped = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setAttribute(QtCore.Qt.WA_StyledBackground)

        self.ui = Ui_CursorControl()
        self.ui.setupUi(self)

        self._manager = CursorManager()

        self._active = False
        self._tracking = False
        self._pos0 = {}
        self._n_trials = 0

    def heightForWidth(self, width):
        return width

    def start(self):
        self._n_trials = 10
        self._manager.reset_cursor()
        self._manager.reset_target()
        self._active = True
        self.update()

    def stop(self):
        self._active = False

    ###########################################################################
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self._active:
            mouse = self._get_mouse_coord(event)
            if abs(self._manager.cursor - mouse) < 0.05:
                self._tracking = True
                self._store_initial_coord(mouse)
            self.update()

    def mouseMoveEvent(self, event):
        if self._tracking:
            coord = self._get_cursor_coord(event)
            self._manager.update_cursor(coord.x, coord.y)
            self._emit('cursor')
            if self._manager.is_close():
                self._n_trials -= 1
                if self._n_trials == 0:
                    self._tracking = False
                    self.stop()
                    self.stopped.emit()
                else:
                    self._manager.reset_target()
                    self._emit('target')
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._tracking = False
            self.update()

    def _emit(self, type_):
        if type_ == 'cursor':
            point = self._manager.cursor
        elif type_ == 'target':
            point = self._manager.target

        self.acquired.emit({
            'type': type_, 'time': time.time(), 'x': point.x, 'y': point.y,
        })

    def _get_mouse_coord(self, event):
        geo = self.frameGeometry()
        return Point2D(event.x() / geo.width(), event.y() / geo.height())

    def _store_initial_coord(self, mouse):
        self._pos0['cursor'] = self._manager.cursor.copy()
        self._pos0['mouse'] = mouse.copy()

    def _get_cursor_coord(self, event):
        mouse = self._get_mouse_coord(event)
        return self._pos0['cursor'] + mouse - self._pos0['mouse']

    ###########################################################################
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        self._draw_grid(painter)
        if self._active:
            self._draw_remaining(painter, event)
            self._draw_cursor(painter, self._manager.cursor, 10)
            self._draw_cursor(painter, self._manager.target, 20)

    def _draw_grid(self, painter):
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()

        pen0 = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
        pen1 = QtGui.QPen(QtCore.Qt.gray, 1, QtCore.Qt.SolidLine)

        for i in range(7):
            painter.setPen(pen0 if i == 3 else pen1)
            r = i * height / 6
            c = i * width / 6
            painter.drawLine(0, r, width, r)
            painter.drawLine(c, 0, c, height)

    def _draw_cursor(self, painter, point, r):
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 3, QtCore.Qt.SolidLine))
        x = point.x * self.frameGeometry().width()
        y = point.y * self.frameGeometry().height()
        painter.drawEllipse(x-r//2, y-r//2, r, r)

    def _draw_remaining(self, painter, event):
        text = str(self._n_trials)
        flag = QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft
        painter.setPen(QtCore.Qt.gray)
        painter.setFont(QtGui.QFont('Decorative', 20))
        painter.drawText(event.rect(), flag, text)
