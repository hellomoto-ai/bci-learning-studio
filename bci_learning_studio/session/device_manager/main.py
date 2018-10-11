"""Implement `device_manager` command"""
import logging

from PyQt5 import QtWidgets

from .DeviceManager import DeviceManager

_LG = logging.getLogger(__name__)


def main(args):
    """Entrypoint for `device_manager`"""
    app = QtWidgets.QApplication(args)
    device_manager = DeviceManager()
    device_manager.show()
    app.exec_()
