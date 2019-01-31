import copy

from PyQt5 import QtWidgets
import numpy as np
import vispy.scene

from bci_learning_studio.qt.sample_viewer.viewer import _apply_filter
import vispy_util


def _get_lim(vals, margin=0.05):
    lim = [np.amin(vals), np.amax(vals)]
    space = (lim[1] - lim[0]) * margin
    lim[0] -= space
    lim[1] += space
    return lim


class _ViewBoxController:
    """Class to controll multiple viewboxes and lines as a group"""
    def __init__(self):
        self._scale = 1.0
        self._lines = []
        self._viewboxes = []
        self._seek_bars = []

        self._x_lim = None
        self._y_lim = None

    @property
    def viewboxes(self):
        return list(self._viewboxes)

    @property
    def seek_bars(self):
        return list(self._seek_bars)

    def append(self, viewbox, line, seek_bar):
        """Add ViewBox and Line object that are controlled by this class."""
        self._viewboxes.append(viewbox)
        self._lines.append(line)
        self._seek_bars.append(seek_bar)

    def _adjust_scale(self, scale):
        """Adjust zoom scale so as not to zoom out too much."""
        scale = max(0.1, scale)
        if self._scale * scale > 1.0:
            scale = 1.0 / self._scale
        return scale

    def zoom(self, scale):
        """Apply zoom to all the ViewBoxes."""
        scale = self._adjust_scale(scale)
        for vbox in self._viewboxes:
            vbox.camera.zoom(factor=[scale, 1], center=vbox.camera.center)
        self._scale *= scale

    def _adjust_pan(self, pan):
        """Adjust pan value so as not to go beyond plot lines."""
        rect = self._viewboxes[0].camera.rect
        overshoot_left = self._x_lim[0] - (rect.left + pan[0])
        if overshoot_left > 0:
            pan[0] += overshoot_left
        overshoot_right = (rect.right + pan[0]) - self._x_lim[1]
        if overshoot_right > 0:
            pan[0] -= overshoot_right
        overshoot_bottom = self._y_lim[0] - (rect.bottom + pan[1])
        if overshoot_bottom > 0:
            pan[1] += overshoot_bottom
        overshoot_top = (rect.top + pan[1]) - self._y_lim[1]
        if overshoot_top > 0:
            pan[1] -= overshoot_top
        return pan

    def pan(self, pan):
        """Apply pan to all the ViewBoxes."""
        pan = self._adjust_pan(pan)
        for vbox in self._viewboxes:
            vbox.camera.pan(pan)

    def set_data(self, x, ys):
        """Set plot Line values."""
        for y, line in zip(ys, self._lines):
            line.set_data(pos=np.vstack((x, y)).T)
        self._x_lim = _get_lim([x], margin=0.05)
        self._y_lim = _get_lim(ys, margin=0.05)

    def reset_range(self):
        """Reset view range"""
        for vbox in self._viewboxes:
            vbox.camera.set_range(x=self._x_lim, y=self._y_lim, margin=0)
        self._scale = 1.0

    def set_seek_bar(self, pos):
        for seek_bar in self._seek_bars:
            seek_bar.set_data(pos)


def _add_plot_components(grid, max_axis_width, line_color, add_seek_bar=True):
    # Add plot line, Y-Axis, and grid
    yaxis = vispy_util.get_axis(orientation='left', minor_tick_length=0)
    yaxis.width_max = max_axis_width

    viewbox = vispy.scene.ViewBox(camera='panzoom')
    line = vispy.scene.visuals.Line(np.array([[0, 0]]), color=line_color)
    viewbox.add(vispy.scene.visuals.GridLines())
    viewbox.add(line)
    seek_bar = None
    if add_seek_bar:
        seek_bar = vispy.scene.visuals.InfiniteLine(pos=0, color=(1, 0, 0, 1))
        viewbox.add(seek_bar)

    grid.add_widget(yaxis, row=0, col=0)
    grid.add_widget(viewbox, row=0, col=1)
    yaxis.link_view(viewbox)
    return viewbox, line, seek_bar


def _add_x_axis(grid, viewbox, max_axis_width):
    dummy = vispy.scene.Widget()
    dummy.width_max = max_axis_width
    grid.add_widget(dummy, row=0, col=0)

    xaxis = vispy_util.get_axis(orientation='bottom')
    xaxis.height_max = max_axis_width
    grid.add_widget(xaxis, row=0, col=1)
    xaxis.link_view(viewbox)


def _create_plots(
        n_plots, widget, interactive,
        axis_width=30, line_color=(0.08, 0.08, 1.0, 0.8)):
    kwargs = {'margin': 0, 'spacing': 0, 'padding': 0}
    base_grid = widget.add_grid(**kwargs)
    ctrl = _ViewBoxController()
    for i in range(n_plots):
        grid = base_grid.add_grid(row=i, col=0, **kwargs)
        viewbox, line, seek_bar = _add_plot_components(
            grid, max_axis_width=axis_width, line_color=line_color,
            add_seek_bar=interactive,
        )
        ctrl.append(viewbox, line, seek_bar)
        if i == 0:
            grid = base_grid.add_grid(row=n_plots, col=0, **kwargs)
            grid.height_max = axis_width
            _add_x_axis(grid, viewbox, max_axis_width=axis_width)
    return ctrl


class _MouseHandler:
    def __init__(self, controller):
        self._ctrl = controller

        self._viewbox_clicked = None
        self._seek_bar_drag = False

    def process_event(self, event, picked):
        if event.type == 'mouse_wheel':
            self._ctrl.zoom(1 + event.delta[1])
        elif event.type == 'mouse_press':
            if picked in self._ctrl.viewboxes:
                self._viewbox_clicked = picked
                self._seek_bar_drag = self._is_seek_bar_clicked(event, picked)
        elif event.type == 'mouse_move' and event.is_dragging:
            if self._seek_bar_drag:
                self._drag_seek_bar(event)
            else:
                self._pan(event, event.last_event)
        elif event.type == 'mouse_release':
            self._viewbox_clicked = None
            self._seek_bar_drag = False

    def _is_seek_bar_clicked(self, event, picked):
        s_ev = vispy.scene.events.SceneMouseEvent(event=event, visual=picked)
        seek_bar = self._ctrl.seek_bars[self._ctrl.viewboxes.index(picked)]
        pos = picked.camera.transform.map(np.asarray([seek_bar.pos, 0, 0, 1]))
        return abs(pos[0] - s_ev.pos[0]) < 3

    def _drag_seek_bar(self, event):
        scene_event = vispy.scene.events.SceneMouseEvent(
            event=event, visual=self._viewbox_clicked)
        coord = self._viewbox_clicked.camera.transform.imap(scene_event.pos)
        self._ctrl.set_seek_bar(coord[0])

    def _pan(self, event, previous_event):
        pos1, pos2 = event.pos, previous_event.pos
        func = self._ctrl.viewboxes[0].camera.transform.imap
        pan = func(np.asarray(pos2[:2])) - func(np.asarray(pos1[:2]))
        self._ctrl.pan(pan)


class Plotter(vispy.scene.SceneCanvas):
    def __init__(self, n_plots=8, interactive=True, **kwargs):
        super().__init__(**kwargs)
        self.unfreeze()

        self.n_plots = n_plots
        self.interactive = interactive

        self._controller = _create_plots(n_plots, self.central_widget, interactive)
        self._mouse_handler = _MouseHandler(self._controller)
        self.central_widget.padding = 15

    def reset_range(self):
        self._controller.reset_range()

    def set_data(self, x, ys):
        self._controller.set_data(x, ys)

    def _process_mouse_event(self, event):
        if self.interactive:
            picked = None
            if event.type == 'mouse_press':
                # visual_at is an expensive operation
                # so only performs when necessary.
                picked = self.visual_at(event.pos)
            self._mouse_handler.process_event(event, picked)
        event.handled = True


def _make_plotter(widget, n_plots, interactive):
    layout = QtWidgets.QVBoxLayout()
    plotter = Plotter(n_plots=n_plots, interactive=interactive)
    layout.addWidget(plotter.native)
    widget.setLayout(layout)
    return plotter


class PlotterWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.plotter = None
        self._eeg_data = None
        self._event_data = None
        self._filter_params = None

    def initialize(self, n_plots, interactive):
        self.plotter = _make_plotter(self, n_plots, interactive)

    @property
    def filter_params(self):
        return copy.deepcopy(self._filter_params)

    def set_data(self, eeg_data, event_data=None):
        self._eeg_data = eeg_data
        self._event_data = event_data
        self._update_plot()

    def set_filter(self, filter_params):
        self._filter_params = filter_params
        self._update_plot()

    def reset_range(self):
        self.plotter.reset_range()

    def _update_plot(self):
        if self._eeg_data:
            x, ys = self._get_plot_data()
            self.plotter.set_data(x, ys)

    def _get_plot_data(self):
        x, ys = self._eeg_data['timestamps'], self._eeg_data['samples']
        if self._filter_params:
            ys = _apply_filter(
                ys, self._filter_params, self._eeg_data['sample_rate'])

        '''
        if self._event_data:
            self._plotter.plot_event(self._event_data['timestamps'])
        if self.interactive:
            self._plotter.seek_bar_dragged.connect(self._seek_bar_dragged)
        '''
        return x, ys
