# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './bci_learning_studio/qt/DeviceManagerWidget_Ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DeviceManagerWidget(object):
    def setupUi(self, DeviceManagerWidget):
        DeviceManagerWidget.setObjectName("DeviceManagerWidget")
        DeviceManagerWidget.resize(594, 297)
        self.verticalLayout = QtWidgets.QVBoxLayout(DeviceManagerWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBoxDeviceList = QtWidgets.QComboBox(DeviceManagerWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxDeviceList.sizePolicy().hasHeightForWidth())
        self.comboBoxDeviceList.setSizePolicy(sizePolicy)
        self.comboBoxDeviceList.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.comboBoxDeviceList.setObjectName("comboBoxDeviceList")
        self.horizontalLayout.addWidget(self.comboBoxDeviceList)
        self.pushButtonRefresh = QtWidgets.QPushButton(DeviceManagerWidget)
        self.pushButtonRefresh.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButtonRefresh.setStyleSheet("")
        self.pushButtonRefresh.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/bci_learning_studio/resource/baseline-refresh-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonRefresh.setIcon(icon)
        self.pushButtonRefresh.setObjectName("pushButtonRefresh")
        self.horizontalLayout.addWidget(self.pushButtonRefresh)
        self.pushButtonConnect = QtWidgets.QPushButton(DeviceManagerWidget)
        self.pushButtonConnect.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButtonConnect.setToolTip("")
        self.pushButtonConnect.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/bci_learning_studio/resource/baseline-phonelink-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonConnect.setIcon(icon1)
        self.pushButtonConnect.setObjectName("pushButtonConnect")
        self.horizontalLayout.addWidget(self.pushButtonConnect)
        spacerItem = QtWidgets.QSpacerItem(269, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.DeviceControllerWidget = DeviceControllerWidget(DeviceManagerWidget)
        self.DeviceControllerWidget.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DeviceControllerWidget.sizePolicy().hasHeightForWidth())
        self.DeviceControllerWidget.setSizePolicy(sizePolicy)
        self.DeviceControllerWidget.setObjectName("DeviceControllerWidget")
        self.verticalLayout.addWidget(self.DeviceControllerWidget)

        self.retranslateUi(DeviceManagerWidget)
        QtCore.QMetaObject.connectSlotsByName(DeviceManagerWidget)

    def retranslateUi(self, DeviceManagerWidget):
        _translate = QtCore.QCoreApplication.translate
        DeviceManagerWidget.setWindowTitle(_translate("DeviceManagerWidget", "Device Manager"))

from bci_learning_studio.qt.DeviceControllerWidget import DeviceControllerWidget
import bci_learning_studio.qt.resource_rc
