import pyqtgraph


class PlotWidget(pyqtgraph.GraphicsLayoutWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent=parent, **kwargs)
