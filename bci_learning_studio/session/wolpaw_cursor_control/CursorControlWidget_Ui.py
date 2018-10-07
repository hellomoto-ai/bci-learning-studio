# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './bci_learning_studio/session/wolpaw_cursor_control/CursorControlWidget_Ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CursorControlWidget(object):
    def setupUi(self, CursorControlWidget):
        CursorControlWidget.setObjectName("CursorControlWidget")
        CursorControlWidget.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(CursorControlWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.cursorControlWidget = QtWidgets.QWidget(CursorControlWidget)
        self.cursorControlWidget.setObjectName("cursorControlWidget")
        self.gridLayout.addWidget(self.cursorControlWidget, 0, 0, 1, 1)

        self.retranslateUi(CursorControlWidget)
        QtCore.QMetaObject.connectSlotsByName(CursorControlWidget)

    def retranslateUi(self, CursorControlWidget):
        _translate = QtCore.QCoreApplication.translate
        CursorControlWidget.setWindowTitle(_translate("CursorControlWidget", "Cursor Control"))

