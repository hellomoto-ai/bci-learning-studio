import os

import umsgpack
import pyqtgraph
from PyQt5 import QtCore, QtGui, QtWidgets

from bci_learning_studio.qt import qt_util, qg_util
from .editor_ui import Ui_Editor


def _ask_open_path(parent):
    options = QtWidgets.QFileDialog.Options(
        QtWidgets.QFileDialog.DontUseNativeDialog
    )
    default_dir = qt_util.get_settings('default_load_dir')
    filename, _ = QtWidgets.QFileDialog.getOpenFileName(
        parent, 'Select recording to edit', default_dir, 'JSON (*.json)',
        options=options)
    if filename:
        qt_util.store_settings(default_load_dir=os.path.dirname(filename))
    return filename


def _load_file(path):
    data = []
    with open(path, 'br') as fileobj:
        while True:
            try:
                data.append(umsgpack.load(fileobj))
            except umsgpack.InsufficientDataException:
                break
    return data


def get_context_menus(parent, n_channels):
    group = QtWidgets.QFrame(parent)
    group.setGeometry(QtCore.QRect(0, 0, 154, 79))
    group.setObjectName('group')
    layout = QtWidgets.QGridLayout(group)
    layout.setObjectName('gridLayout')
    for i in range(n_channels):
        check = QtWidgets.QCheckBox(group)
        check.setObjectName('plot%s' % i)
        check.setText('Plot %s' % i)
        layout.addWidget(check, i, 0, 1, 1)
    return group


class Editor(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)

        self.ui = Ui_Editor()
        self.ui.setupUi(self)

        self.ui.actionOpen.triggered.connect(self._open_file)

        qt_util.restore_window_position(self)

        self._filename = None
        self._eeg_data = []
        self._cursor_data = []
        self._target_data = []
        self._bar = None

    ###########################################################################
    # Misc
    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        qt_util.store_window_position(self)
        self.parent().show()
        event.accept()

    def _center_replay(self):
        this_w = self.frameGeometry().width()
        geo = self.ui.cursorReplay.frameGeometry()
        rep_w, rep_h = geo.width(), geo.height()
        diff = (this_w - geo.width()) // 2
        self.ui.cursorReplay.setGeometry(diff, 0, rep_w, rep_h)
        self.update()
        geo = self.ui.cursorReplay.frameGeometry()

    ###########################################################################
    def _open_file(self, _):
        self._filename = _ask_open_path(self)
        if self._filename:
            self._load_file(self._filename)

    def _load_file(self, path):
        data = _load_file(path)
        self._eeg_data = []
        self._cursor_data = []
        self._target_data = []
        target_x, target_y = 0.0, 0.0
        for datum in data:
            if 'eeg' in datum:
                self._eeg_data.append(datum)
            elif datum['type'] == 'cursor':
                datum['target_x'] = target_x
                datum['target_y'] = target_y
                self._cursor_data.append(datum)
            elif datum['type'] == 'target':
                self._target_data.append(datum)
                target_x = datum['x']
                target_y = datum['y']
        self._plot()

    def _plot(self):
        self.ui.graphWidget.clear()
        plot = self.ui.graphWidget.addPlot(
            row=1, col=1, title=os.path.split(self._filename)[-1],
            axisItems={'bottom': qg_util.TimeAxisItem(orientation='bottom')},
        )
        plot.showGrid(x=True, y=True, alpha=1)
        plot.setMouseEnabled(x=True, y=False)

        x_min, x_max = float('inf'), 0.0
        y_min, y_max = float('inf'), 0.0
        for i in range(16):
            x = [d['timestamp'] for d in self._eeg_data]
            y = [d['eeg'][i] for d in self._eeg_data]
            plot.plot(x, y, pen=pyqtgraph.mkPen(color=(0, 0, 255), width=3))
            x_min = min(x_min, min(x))
            x_max = max(x_max, max(x))
            y_min = min(y_min, min(y))
            y_max = max(y_max, max(y))
        max_x_range = 1.1 * (x_max - x_min)
        min_x = x_max - max_x_range
        max_x = x_min + max_x_range
        plot.getViewBox().setLimits(
            maxXRange=max_x_range, xMin=min_x, xMax=max_x)
        menu = plot.getMenu()
        # TODO: Add plot reaction
        grp = get_context_menus(menu, 16)
        name = 'Data'
        sm = QtGui.QMenu(name)
        act = QtGui.QWidgetAction(plot)
        act.setDefaultWidget(grp)
        sm.addAction(act)
        plot.subMenus.append(sm)
        plot.ctrlMenu.addMenu(sm)

        for datum in self._target_data:
            plot.addLine(
                x=datum['time'],
                pen=pyqtgraph.mkPen(color=(0, 128, 0), width=3),
                markers=[('o', 0.0, 10.0), ('o', 1.0, 10.0)],
            )
        self._bar = plot.addLine(
            x=x_min, pen=pyqtgraph.mkPen(color=(0, 0, 0), width=3),
            movable=True, bounds=[x_min, x_max],
            markers=[('^', 0.0, 10.0), ('v', 1.0, 10.0)],
        )
        self._bar.sigDragged.connect(self._update_replay)

        self.ui.cursorReplay.set_cursor(x=0, y=1)
        self.ui.cursorReplay.set_target(x=0, y=0.5)
        self.ui.cursorReplay.update()

    ##########################################################################
    def _update_replay(self):
        timestamp = self._bar.getXPos()
        cursor = self._get_cursor_data(timestamp)
        if cursor:
            self.ui.cursorReplay.set_cursor(x=cursor['x'], y=cursor['y'])
            self.ui.cursorReplay.set_target(
                x=cursor['target_x'], y=cursor['target_y'])
            self.ui.cursorReplay.update()

    def _get_cursor_data(self, timestamp):
        ret = self._cursor_data[0]
        for datum in self._cursor_data:
            if datum['time'] > timestamp:
                return ret
            ret = datum
