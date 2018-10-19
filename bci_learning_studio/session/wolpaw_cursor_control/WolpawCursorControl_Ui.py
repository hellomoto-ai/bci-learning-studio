# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './bci_learning_studio/session/wolpaw_cursor_control/WolpawCursorControl_Ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WolpawCursorControl(object):
    def setupUi(self, WolpawCursorControl):
        WolpawCursorControl.setObjectName("WolpawCursorControl")
        WolpawCursorControl.resize(800, 769)
        self.centralwidget = QtWidgets.QWidget(WolpawCursorControl)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.deviceManagerWidget = DeviceManagerWidget(self.centralwidget)
        self.deviceManagerWidget.setMinimumSize(QtCore.QSize(200, 400))
        self.deviceManagerWidget.setMaximumSize(QtCore.QSize(400, 16777215))
        self.deviceManagerWidget.setObjectName("deviceManagerWidget")
        self.horizontalLayout.addWidget(self.deviceManagerWidget, 0, QtCore.Qt.AlignLeft)
        self.widget = CursorControlWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.horizontalLayout.addWidget(self.widget)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.logWidget = LogWidget(self.centralwidget)
        self.logWidget.setMinimumSize(QtCore.QSize(0, 300))
        self.logWidget.setMaximumSize(QtCore.QSize(16777215, 300))
        self.logWidget.setObjectName("logWidget")
        self.verticalLayout_2.addWidget(self.logWidget)
        WolpawCursorControl.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(WolpawCursorControl)
        self.statusbar.setObjectName("statusbar")
        WolpawCursorControl.setStatusBar(self.statusbar)

        self.retranslateUi(WolpawCursorControl)
        QtCore.QMetaObject.connectSlotsByName(WolpawCursorControl)

    def retranslateUi(self, WolpawCursorControl):
        _translate = QtCore.QCoreApplication.translate
        WolpawCursorControl.setWindowTitle(_translate("WolpawCursorControl", "Wolpaw Cursol Control"))

from bci_learning_studio.qt.DeviceManagerWidget import DeviceManagerWidget
from bci_learning_studio.qt.LogWidget import LogWidget
from bci_learning_studio.session.wolpaw_cursor_control.CursorControlWidget import CursorControlWidget
