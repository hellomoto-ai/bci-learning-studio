import argparse

from PyQt5 import QtWidgets
import pyqtgraph

from .mode_selector import ModeSelector
from .editor import Editor
from .recorder import Recorder


def _parse_args(args):
    parser = argparse.ArgumentParser(
        description='Launch cursor control Recorder/Editor.'
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--recorder', action='store_true',
        help='Launch recorder directly.'
    )
    group.add_argument(
        '--editor', action='store_true',
        help='Launch editor directly.'
    )
    return parser.parse_known_args(args)


def main(args):
    namespace, args = _parse_args(args)

    pyqtgraph.setConfigOption('background', 'w')
    pyqtgraph.setConfigOption('foreground', 'k')

    if namespace.editor:
        window_class = Editor
    elif namespace.recorder:
        window_class = Recorder
    else:
        window_class = ModeSelector

    app = QtWidgets.QApplication(args)
    app.setOrganizationName('hellomoto')
    app.setApplicationName('bci_learning_studio.cursor_control')
    window = window_class()
    window.show()
    return app.exec_()
