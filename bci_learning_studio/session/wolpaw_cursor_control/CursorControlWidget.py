from PyQt5 import QtWidgets, QtGui, QtCore

from .CursorControlWidget_Ui import Ui_CursorControlWidget


class CursorControlWidget(QtGui.QWidget, Ui_CursorControlWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()
        
    def drawText(self, event, qp):
        qp.setPen(QtGui.QColor(168, 34, 3))
        qp.setFont(QtGui.QFont('Decorative', 10))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, 'foo')
