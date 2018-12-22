import time

from PyQt5 import QtWidgets, QtCore, QtGui

from .cursors import Point2D, CursorManager


class _Tracker:
    def __init__(self, cursor_manager):
        self.cursor_manager = cursor_manager
        self.height = None
        self.width = None

        self.active = False
        self.tracking = False
        self._pos0 = {}

    def activate(self):
        self.active = True

    def deactivate(self):
        self.tracking = False
        self.active = False

    def start_tracking(self, mouse):
        self.tracking = True
        self._pos0['cursor'] = self.cursor_manager.cursor.copy()
        self._pos0['mouse'] = mouse

    def stop_tracking(self):
        self.tracking = False

    def process_press_event(self, event, geometry):
        self.width, self.height = geometry.width(), geometry.height()

        mouse = Point2D(event.x() / self.width, event.y() / self.height)
        if abs(self.cursor_manager.cursor - mouse) < 0.05:
            self.start_tracking(mouse)

    def process_move_event(self, event):
        mouse = Point2D(event.x() / self.width, event.y() / self.height)
        cursor = self._pos0['cursor'] + mouse - self._pos0['mouse']
        self.cursor_manager.update_cursor(cursor.x, cursor.y)


class CursorControl(QtWidgets.QWidget):
    acquired = QtCore.pyqtSignal(dict)
    stopped = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setAttribute(QtCore.Qt.WA_StyledBackground)

        self._manager = CursorManager()

        self._tracker = _Tracker(self._manager)
        self._n_trials = 0

    def heightForWidth(self, width):
        return width

    ##########################################################################
    def start(self):
        self._manager.reset_cursor()
        self._manager.reset_target()
        self._tracker.activate()
        self._n_trials = 10
        self.update()

    def stop(self):
        self._tracker.stop_tracking()
        self._tracker.deactivate()

    ###########################################################################
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self._tracker.active:
            self._tracker.process_press_event(event, self.frameGeometry())
            event.accept()

    def mouseMoveEvent(self, event):
        if self._tracker.tracking:
            self._tracker.process_move_event(event)
            self._emit('cursor')
            if self._manager.is_close():
                self._manager.reset_target()
                self._n_trials -= 1
                if self._n_trials == 0:
                    self.stop()
                    self.stopped.emit()
                else:
                    self._emit('target')
            event.accept()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._tracker.stop_tracking()
            event.accept()

    def _emit(self, type_):
        if type_ == 'target':
            self.acquired.emit({
                'type': type_,
                'data': {
                    'time': time.time(),
                    'x': self._manager.target.x,
                    'y': self._manager.target.y,
                },
            })
        elif type_ == 'cursor':
            self.acquired.emit({
                'type': type_,
                'data': {
                    'time': time.time(),
                    'x': self._manager.cursor.x,
                    'y': self._manager.cursor.y,
                    'target_x': self._manager.target.x,
                    'target_y': self._manager.target.y,
                },
            })

    ###########################################################################
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        self._manager.draw(painter, self.frameGeometry())
        self._draw_remaining(painter, event)

    def _draw_remaining(self, painter, event):
        text = str(self._n_trials)
        flag = QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft
        painter.setPen(QtCore.Qt.gray)
        painter.setFont(QtGui.QFont('Decorative', 20))
        painter.drawText(event.rect(), flag, text)
