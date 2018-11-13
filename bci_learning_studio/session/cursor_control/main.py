from PyQt5 import QtWidgets
import pyqtgraph

from .mode_selector import ModeSelector


def main(args):
    pyqtgraph.setConfigOption('background', 'w')
    pyqtgraph.setConfigOption('foreground', 'k')

    app = QtWidgets.QApplication(args)
    app.setOrganizationName('hellomoto')
    app.setApplicationName('bci_learning_studio.cursor_control')
    window = ModeSelector()
    window.show()
    return app.exec_()
