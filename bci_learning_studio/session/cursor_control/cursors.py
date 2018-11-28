import numpy as np

from PyQt5 import QtGui, QtCore


class Point2D:
    def __init__(self, x=0, y=0):
        self._data = np.asarray([x, y])

    @property
    def x(self):
        return self._data[0]

    @property
    def y(self):
        return self._data[1]

    @x.setter
    def x(self, val):
        self._data[0] = val

    @y.setter
    def y(self, val):
        self._data[1] = val

    def __abs__(self):
        return np.linalg.norm(self._data)

    def __add__(self, other):
        return Point2D(x=self.x+other.x, y=self.y+other.y)

    def __sub__(self, other):
        return Point2D(x=self.x-other.x, y=self.y-other.y)

    def copy(self):
        return Point2D(x=self.x, y=self.y)


def _draw_cursor(
        painter, width, height, point, diameter, color, x_offset, y_offset):
    painter.setPen(QtGui.QPen(color, 3, QtCore.Qt.SolidLine))
    painter.setBrush(color)
    _x = x_offset + point.x * width
    _y = y_offset + point.y * height
    radius = diameter // 2
    painter.drawEllipse(_x-radius, _y-radius, diameter, diameter)


def _draw_grid(painter, width, height, x_offset, y_offset):
    pen0 = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
    pen1 = QtGui.QPen(QtCore.Qt.gray, 1, QtCore.Qt.SolidLine)

    painter.setBrush(QtCore.Qt.white)
    painter.drawRect(x_offset, y_offset, width, height)
    for i in range(7):
        painter.setPen(pen0 if i == 3 else pen1)
        row = i * height / 6
        col = i * width / 6
        # horizongal
        painter.drawLine(
            x_offset, y_offset + row,
            x_offset + width, y_offset + row)
        # vertical
        painter.drawLine(
            x_offset + col, y_offset + 0,
            x_offset + col, y_offset + height)


class CursorManager:
    def __init__(self, threshold=0.02, random_seed=None):
        self.cursor = Point2D(0.5, 0.5)
        self.target = Point2D(0.5, 0.5)
        self.threshold = threshold
        self.rng = np.random.RandomState(random_seed)

    def update_cursor(self, x, y):
        self.cursor.x = x
        self.cursor.y = y

    def reset_cursor(self):
        self.cursor = Point2D(0.5, 0.5)

    def reset_target(self):
        self.target = Point2D(self.rng.uniform(0, 1), self.rng.uniform(0, 1))

    def is_close(self):
        return abs(self.cursor - self.target) < self.threshold

    def draw(self, painter, geometry):
        width, height = geometry.width(), geometry.height()
        length = min(geometry.width(), geometry.height())
        x_offset = (width - length) // 2
        y_offset = (height - length) // 2
        _draw_grid(painter, length, length, x_offset, y_offset)
        _draw_cursor(
            painter, length, length, self.target, 20, QtCore.Qt.blue,
            x_offset, y_offset)
        _draw_cursor(
            painter, length, length, self.cursor, 10, QtCore.Qt.black,
            x_offset, y_offset)
