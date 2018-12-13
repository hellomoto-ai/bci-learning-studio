from PyQt5 import QtWidgets, QtGui


_RAILED = 'railed'
_NEAR_RAILED = 'near_railed'
_OK = 'ok'

_RED = QtGui.QColor(255, 0, 0, 255)
_YELLOW = QtGui.QColor(255, 255, 0, 255)
_GREEN = QtGui.QColor(0, 255, 0, 255)
_GRAY = QtGui.QColor(160, 160, 160, 255)
_DARK = QtGui.QColor(130, 130, 130, 255)


class MeasurementStatusIndicator(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(QtWidgets.QWidget, self).__init__(parent)

        self._status = None

    def heightForWidth(self, width):
        return width

    def reset_status(self):
        self._status = None

    def set_railed(self):
        self._status = _RAILED

    def set_near_railed(self):
        self._status = _NEAR_RAILED

    def set_ok(self):
        self._status = _OK

    def paintEvent(self, ev):
        super().paintEvent(ev)

        geo = self.geometry()
        width, height = geo.width(), geo.height()
        radius = 0.8 * min(width, height)
        _x, _y = (width - radius) / 2, (height - radius) / 2

        if self._status == _RAILED:
            color = _RED
        elif self._status == _NEAR_RAILED:
            color = _YELLOW
        elif self._status == _OK:
            color = _GREEN
        else:
            color = _GRAY

        p = QtGui.QPainter(self)
        p.setPen(_DARK)
        p.setBrush(color)
        p.drawEllipse(_x, _y, radius, radius)
