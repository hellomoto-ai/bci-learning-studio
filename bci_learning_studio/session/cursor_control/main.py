from PyQt5 import QtWidgets

from .main_window import MainWindow


def main(args):
    app = QtWidgets.QApplication(args)
    app.setOrganizationName('hellomoto')
    app.setApplicationName('bci_learning_studio.cursor_control')
    window = MainWindow()
    window.show()
    return app.exec_()
