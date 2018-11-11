import numpy as np


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
