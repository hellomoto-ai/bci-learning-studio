from PyQt5 import QtWidgets

from .PlotWindow_Ui import Ui_Plot


class PlotWindow(QtWidgets.QMainWindow, Ui_Plot):
    def __init__(self, parent=None):
        super(PlotWindow, self).__init__(parent)
        self.setupUi(self)
