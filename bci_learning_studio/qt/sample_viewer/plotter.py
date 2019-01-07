from datetime import datetime

import numpy as np
from PyQt5 import QtCore, QtGui
import pyqtgraph as pg


def _get_locations(val_range, min_lines=None, max_lines=None):
    dist = val_range[1] - val_range[0]
    interval = 10. ** np.floor(np.log10(dist))
    n_lines = dist // interval + 1
    while min_lines and n_lines <= min_lines:
        interval /= 2
        n_lines = dist // interval + 1
    while max_lines and n_lines >= max_lines:
        interval *= 2
        n_lines = dist // interval + 1
    start = interval * (val_range[0] // interval)
    end = interval * (val_range[1] // interval + 1)
    return np.arange(start, end, interval)


class _GridItem(pg.UIGraphicsItem):
    def __init__(self, x_label, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.x_label = x_label

    def paint(self, p, option, widget):
        picture = self.generatePicture()
        p.drawPicture(QtCore.QPointF(0, 0), picture)

    def generatePicture(self):
        rect = self.boundingRect()
        x_range = [rect.left(), rect.right()]
        y_range = [rect.top(), rect.bottom()]

        x_vals = _get_locations(x_range, min_lines=4)
        y_vals = _get_locations(y_range, max_lines=4)

        picture = QtGui.QPicture()
        painter = QtGui.QPainter()
        painter.begin(picture)
        self._draw_vlines(painter, x_vals, y_range)
        self._draw_hlines(painter, x_range, y_vals)
        trans = self.deviceTransform()
        painter.setWorldTransform(pg.functions.invertQTransform(trans))
        if self.x_label:
            self._draw_vtexts(painter, x_vals, y_range, trans)
        self._draw_htexts(painter, x_range, y_vals, trans)
        painter.end()
        return picture

    def _draw_vlines(self, painter, x_vals, y_range):
        pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 50))
        pen.setWidthF(self.pixelWidth())
        painter.setPen(pen)
        for val in x_vals:
            painter.drawLine(
                QtCore.QPointF(val, y_range[0]),
                QtCore.QPointF(val, y_range[1]),
            )

    def _draw_vtexts(self, painter, x_vals, y_range, trans):
        pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 90))
        pen.setWidthF(self.pixelWidth())
        painter.setPen(pen)
        painter.setFont(QtGui.QFont('Aerial', 9))
        for val in x_vals:
            point = QtCore.QPointF(val, y_range[0])
            point = trans.map(point) + pg.Point(0.3, -0.3)
            fraction = int((1000 * val) % 1000)
            text = datetime.fromtimestamp(val).strftime(
                '%H:%M:%S.{:d}'.format(fraction))
            painter.drawText(point, text)

    def _draw_hlines(self, painter, x_range, y_vals):
        pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 50))
        pen.setWidthF(self.pixelHeight())
        painter.setPen(pen)
        for val in y_vals:
            painter.drawLine(
                QtCore.QPointF(x_range[0], val),
                QtCore.QPointF(x_range[1], val),
            )

    def _draw_htexts(self, painter, x_range, y_vals, trans):
        pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 90))
        pen.setWidthF(self.pixelHeight())
        painter.setPen(pen)
        painter.setFont(QtGui.QFont('Aerial', 9))
        for val in y_vals:
            point = QtCore.QPointF(x_range[0], val)
            point = trans.map(point) + pg.Point(7, -0.5)
            painter.drawText(point, '%g' % val)


class _ViewBox(pg.ViewBox):
    mouse_dragged = QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, enableMouse=False, **kwargs)

    def wheelEvent(self, event):
        # wheelEvent is handled by PlotterWidget
        event.ignore()

    def mouseDragEvent(self, event):
        self.mouse_dragged.emit(event)
        event.accept()

    def auto_range(self):
        x_range_min = self.state['viewRange'][0][0]
        x_range_max = self.state['viewRange'][0][1]
        # Get data
        for child in self.allChildren():
            if isinstance(child, pg.PlotCurveItem):
                data_shown = child.yData[np.where(
                    (x_range_min < child.xData) &
                    (child.xData < x_range_max)
                )]
                if data_shown.size:
                    y_range_min = np.amin(data_shown)
                    y_range_max = np.amax(data_shown)
                    y_range = 1.03 * (y_range_max - y_range_min)
                    y_range_min = np.amax(data_shown) - y_range
                    y_range_max = np.amin(data_shown) + y_range
                    self.setRange(yRange=(y_range_min, y_range_max))
                break


def _get_plot_item(x, y, name, x_label):
    view_box = _ViewBox(
        border=QtGui.QColor(0, 0, 0, alpha=80),
    )
    curve = pg.PlotCurveItem(
        x, y, name=name,
        downsampleMethod='peak', autoDownsample=True,
        pen=pg.mkPen(color=(0, 0, 0xFF, 0x80)),
    )
    grid = _GridItem(x_label=x_label)
    view_box.addItem(curve)
    view_box.addItem(grid)
    return view_box, curve


class PlotterWidget(pg.GraphicsLayout):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self._view_boxes = []
        self._curves = []

    def plot(self, x, ys):
        self.clear()
        self._view_boxes = []
        self._curves = []

        for i, y in enumerate(ys, start=1):
            view_box, curve = _get_plot_item(
                x, y, name='Channel %s' % i, x_label=i == len(ys))
            self.addItem(view_box, row=i, col=0)
            self._view_boxes.append(view_box)
            self._curves.append(curve)

    def plot_event(self, xs):
        if not self._view_boxes:
            return

        vb = self._view_boxes[0]
        for x in xs:
            line = pg.InfiniteLine(
                pos=x, pen=pg.mkPen(color=(92, 128, 92), width=2),
                markers=[('^', 0.0, 4.0), ('v', 1.0, 4.0)],
            )
            vb.addItem(line, ignoreBounds=False)

    def setData(self, x, ys):
        if len(self._curves) == len(ys):
            for y, curve in zip(ys, self._curves):
                curve.setData(x, y)
        else:
            self.plot(x, ys)

    def auto_range(self):
        for vb in self._view_boxes:
            vb.auto_range()


class InteractivePlotterWidget(PlotterWidget):
    seek_bar_dragged = QtCore.pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._seek_bar = None
        self._scale = 1.0

    def plot(self, x, ys):
        super().plot(x, ys)
        x_min, x_max = np.amin(x), np.amax(x)
        self._set_limit(x_min, x_max)
        self._add_seek_bar(x_min, x_max)
        self._add_mouse_drag()

    def _set_limit(self, x_min, x_max):
        x_range = 1.01 * (x_max - x_min)
        x_max = x_min + x_range
        for view_box in self._view_boxes:
            view_box.setLimits(maxXRange=x_range, xMin=x_min, xMax=x_max)

    def _add_seek_bar(self, x_min, x_max):
        self._seek_bar = pg.InfiniteLine(
            pos=x_min, pen=pg.mkPen(color=(0, 0, 0), width=3),
            movable=True, bounds=[x_min, x_max],
            markers=[('^', 0.0, 4.0), ('v', 1.0, 4.0)],
        )
        self._seek_bar.sigDragged.connect(self._seek_bar_dragged)
        self._view_boxes[0].addItem(self._seek_bar)

    def _seek_bar_dragged(self, line):
        self.seek_bar_dragged.emit(line.getXPos())

    def _add_mouse_drag(self):
        for view_box in self._view_boxes:
            view_box.mouse_dragged.connect(self.mouse_drag_event)

    def wheelEvent(self, event):
        event.accept()
        if not self._view_boxes:
            return

        delta = event.delta()
        if abs(delta) < 3:
            return

        if event.orientation() == QtCore.Qt.Vertical:
            scale = 1.01 ** (delta / 8.0)
            if self._scale * scale > 1.0:
                return
            for view_box in self._view_boxes:
                view_box.scaleBy(x=scale)
            self._scale *= scale
        else:
            self._pan_views(pg.Point(-delta, 0))
        self.auto_range()

    def mouse_drag_event(self, event):
        if not self._view_boxes:
            return

        if event.button() == QtCore.Qt.LeftButton:
            self._pan_views(event.lastPos()-event.pos())
            self.auto_range()

    def _pan_views(self, diff):
        view_box = self._view_boxes[0]
        trans = view_box.mapToView(diff) - view_box.mapToView(pg.Point(0, 0))
        x_ = trans.x()
        for view_box in self._view_boxes:
            view_box.translateBy(x=x_, y=0)
