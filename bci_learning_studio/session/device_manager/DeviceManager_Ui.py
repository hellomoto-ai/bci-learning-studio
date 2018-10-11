# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './bci_learning_studio/session/device_manager/DeviceManager_Ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DeviceManager(object):
    def setupUi(self, DeviceManager):
        DeviceManager.setObjectName("DeviceManager")
        DeviceManager.resize(575, 429)
        self.centralwidget = QtWidgets.QWidget(DeviceManager)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.widget = DeviceManagerWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)
        DeviceManager.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(DeviceManager)
        self.statusbar.setObjectName("statusbar")
        DeviceManager.setStatusBar(self.statusbar)

        self.retranslateUi(DeviceManager)
        QtCore.QMetaObject.connectSlotsByName(DeviceManager)

    def retranslateUi(self, DeviceManager):
        _translate = QtCore.QCoreApplication.translate
        DeviceManager.setWindowTitle(_translate("DeviceManager", "Device Manager"))

from bci_learning_studio.qt.DeviceManagerWidget import DeviceManagerWidget
