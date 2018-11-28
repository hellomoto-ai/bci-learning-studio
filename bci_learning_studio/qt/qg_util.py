import datetime

import pyqtgraph
from pyqtgraph.Qt import QtCore, QtGui


def _int2dt(timestamp):
    return datetime.datetime.utcfromtimestamp(float(timestamp))


class TimeAxisItem(pyqtgraph.AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        return [_int2dt(value).strftime('%H:%M:%S') for value in values]


class DraggableLine(pyqtgraph.GraphItem):
    def __init__(self, x=0.0, y=0.0):
        super().__init__()

        self._drag_point = None
        self._drag_offset = None

    def mouseDragEvent(self, event):
        if event.button() != QtCore.Qt.LeftButton:
            event.ignore()
            return

        if event.isStart():
            pos = event.buttonDownPos()
            pts = self.scatter.pointsAt(pos)
            if not pts:
                event.ignore()
                return
            self._drag_point = pts[0]
            index = pts[0].data()[0]
            self._drag_offset = self.data['pos'][index][1] - pos[1]
        elif event.isFinish():
            self._drag_point = None
            return
        else:
            if self._drag_point is None:
                event.ignore()
                return

        ind = self._drag_point.data()[0]
        self.data['pos'][ind][1] = event.pos()[1] + self.dragOffset
        self.updateGraph()
        event.accept()
