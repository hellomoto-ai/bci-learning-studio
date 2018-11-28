# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './bci_learning_studio/qt/device_status_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DeviceStatus(object):
    def setupUi(self, DeviceStatus):
        DeviceStatus.setObjectName("DeviceStatus")
        DeviceStatus.resize(540, 136)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DeviceStatus.sizePolicy().hasHeightForWidth())
        DeviceStatus.setSizePolicy(sizePolicy)
        DeviceStatus.setMaximumSize(QtCore.QSize(16777215, 136))
        self.verticalLayout = QtWidgets.QVBoxLayout(DeviceStatus)
        self.verticalLayout.setContentsMargins(-1, 0, -1, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(DeviceStatus)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.boardInfo = QtWidgets.QTextEdit(DeviceStatus)
        self.boardInfo.setMaximumSize(QtCore.QSize(16777215, 80))
        font = QtGui.QFont()
        font.setFamily("Courier")
        self.boardInfo.setFont(font)
        self.boardInfo.setReadOnly(True)
        self.boardInfo.setObjectName("boardInfo")
        self.verticalLayout.addWidget(self.boardInfo)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(DeviceStatus)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.sampleRate = QtWidgets.QLabel(DeviceStatus)
        self.sampleRate.setObjectName("sampleRate")
        self.horizontalLayout.addWidget(self.sampleRate)
        self.label_3 = QtWidgets.QLabel(DeviceStatus)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.boardInfo.raise_()
        self.label_2.raise_()

        self.retranslateUi(DeviceStatus)
        QtCore.QMetaObject.connectSlotsByName(DeviceStatus)

    def retranslateUi(self, DeviceStatus):
        _translate = QtCore.QCoreApplication.translate
        DeviceStatus.setWindowTitle(_translate("DeviceStatus", "Form"))
        self.label_2.setText(_translate("DeviceStatus", "Board:"))
        self.label.setText(_translate("DeviceStatus", "Sampling Rate:"))
        self.sampleRate.setText(_translate("DeviceStatus", "0"))
        self.label_3.setText(_translate("DeviceStatus", "Hz"))

