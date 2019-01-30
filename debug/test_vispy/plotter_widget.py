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
        self.scale = 1.0
        self._lines = []
        self._viewboxes = []
        self._x_lim = None
        self._y_lim = None

    def append(self, viewbox, line):
        """Add ViewBox and Line object that are controlled by this class."""
        self._viewboxes.append(viewbox)
        self._lines.append(line)

    def _adjust_scale(self, scale):
        """Adjust zoom scale so as not to zoom out too much."""
        scale = max(0.1, scale)
        if self.scale * scale > 1.0:
            scale = 1.0 / self.scale
        return scale

    def zoom(self, scale):
        """Apply zoom to all the ViewBoxes."""
        scale = self._adjust_scale(scale)
        for vbox in self._viewboxes:
            vbox.camera.zoom(factor=[scale, 1], center=vbox.camera.center)
        self.scale *= scale

    def get_pan(self, event, previous_event):
        """Get pan value between two mouse events."""
        pos1, pos2 = event.pos, previous_event.pos
        func = self._viewboxes[0].camera.transform.imap
        return func(np.asarray(pos2[:2])) - func(np.asarray(pos1[:2]))

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
        self.scale = 1.0


def _add_plot_components(grid, max_axis_width, line_color):
    # Add plot line, Y-Axis, and grid
    yaxis = vispy_util.get_axis(orientation='left', minor_tick_length=0)
    yaxis.width_max = max_axis_width

    viewbox = vispy.scene.ViewBox(camera='panzoom')
    line = vispy.scene.visuals.Line(np.array([[0, 0]]), color=line_color)
    viewbox.add(vispy.scene.visuals.GridLines())
    viewbox.add(line)

    grid.add_widget(yaxis, row=0, col=0)
    grid.add_widget(viewbox, row=0, col=1)
    yaxis.link_view(viewbox)
    return viewbox, line


def _add_x_axis(grid, viewbox, max_axis_width):
    dummy = vispy.scene.Widget()
    dummy.width_max = max_axis_width
    grid.add_widget(dummy, row=0, col=0)

    xaxis = vispy_util.get_axis(orientation='bottom')
    xaxis.height_max = max_axis_width
    grid.add_widget(xaxis, row=0, col=1)
    xaxis.link_view(viewbox)


def _create_plots(
        n_plots, widget,
        axis_width=30, line_color=(0.08, 0.08, 1.0, 0.8)):
    kwargs = {'margin': 0, 'spacing': 0, 'padding': 0}
    base_grid = widget.add_grid(**kwargs)
    ctrl = _ViewBoxController()
    for i in range(n_plots):
        grid = base_grid.add_grid(row=i, col=0, **kwargs)
        viewbox, line = _add_plot_components(
            grid, max_axis_width=axis_width, line_color=line_color)
        ctrl.append(viewbox, line)
        if i == 0:
            grid = base_grid.add_grid(row=n_plots, col=0, **kwargs)
            grid.height_max = axis_width
            _add_x_axis(grid, viewbox, max_axis_width=axis_width)
    return ctrl


class Plotter(vispy.scene.SceneCanvas):
    def __init__(self, n_plots=8, interactive=True, **kwargs):
        super().__init__(**kwargs)
        self.unfreeze()

        self.n_plots = n_plots
        self.interactive = interactive

        self._controller = _create_plots(n_plots, self.central_widget)
        self.central_widget.padding = 15

    def reset_range(self):
        self._controller.reset_range()

    def set_data(self, x, ys):
        self._controller.set_data(x, ys)

    def _process_mouse_event(self, event):
        if self.interactive:
            if event.type == 'mouse_wheel':
                self._controller.zoom(1 + event.delta[1])
            elif event.type == 'mouse_move' and event.is_dragging:
                pan = self._controller.get_pan(event, event.last_event)
                self._controller.pan(pan)
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
