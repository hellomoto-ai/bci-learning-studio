"""Implement `device_manager` command"""
import logging

from PyQt5 import QtWidgets

from bci_learning_studio.qt.device_manager import DeviceManager

_LG = logging.getLogger(__name__)


def main(args):
    """Entrypoint for `device_manager`"""
    app = QtWidgets.QApplication(args)
    app.setOrganizationName('hellomoto')
    app.setApplicationName('bci_learning_studio.device_manager')
    device_manager = DeviceManager()
    device_manager.show()
    return app.exec_()
