# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './bci_learning_studio/qt/device_manager/device_selector_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DeviceSelector(object):
    def setupUi(self, DeviceSelector):
        DeviceSelector.setObjectName("DeviceSelector")
        DeviceSelector.resize(289, 87)
        DeviceSelector.setModal(True)
        self.deviceList = QtWidgets.QComboBox(DeviceSelector)
        self.deviceList.setGeometry(QtCore.QRect(10, 10, 211, 26))
        self.deviceList.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.deviceList.setObjectName("deviceList")
        self.connectButton = QtWidgets.QPushButton(DeviceSelector)
        self.connectButton.setGeometry(QtCore.QRect(170, 50, 113, 32))
        self.connectButton.setObjectName("connectButton")

        self.retranslateUi(DeviceSelector)
        QtCore.QMetaObject.connectSlotsByName(DeviceSelector)

    def retranslateUi(self, DeviceSelector):
        _translate = QtCore.QCoreApplication.translate
        DeviceSelector.setWindowTitle(_translate("DeviceSelector", "Select Device"))
        self.connectButton.setText(_translate("DeviceSelector", "Connect"))

