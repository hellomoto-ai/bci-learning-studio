# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './bci_learning_studio/qt/device_manager/device_status_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DeviceStatus(object):
    def setupUi(self, DeviceStatus):
        DeviceStatus.setObjectName("DeviceStatus")
        DeviceStatus.resize(540, 118)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DeviceStatus.sizePolicy().hasHeightForWidth())
        DeviceStatus.setSizePolicy(sizePolicy)
        DeviceStatus.setMaximumSize(QtCore.QSize(16777215, 118))
        self.verticalLayout = QtWidgets.QVBoxLayout(DeviceStatus)
        self.verticalLayout.setContentsMargins(-1, 0, -1, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_board = QtWidgets.QLabel(DeviceStatus)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_board.setFont(font)
        self.label_board.setObjectName("label_board")
        self.horizontalLayout_2.addWidget(self.label_board)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.sampleRate = QtWidgets.QLabel(DeviceStatus)
        self.sampleRate.setObjectName("sampleRate")
        self.horizontalLayout_2.addWidget(self.sampleRate)
        self.label_hz = QtWidgets.QLabel(DeviceStatus)
        self.label_hz.setObjectName("label_hz")
        self.horizontalLayout_2.addWidget(self.label_hz)
        self.measurementStatusIndicator = MeasurementStatusIndicator(DeviceStatus)
        self.measurementStatusIndicator.setMinimumSize(QtCore.QSize(40, 20))
        self.measurementStatusIndicator.setObjectName("measurementStatusIndicator")
        self.horizontalLayout_2.addWidget(self.measurementStatusIndicator)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.boardInfo = QtWidgets.QTextEdit(DeviceStatus)
        self.boardInfo.setMaximumSize(QtCore.QSize(16777215, 90))
        font = QtGui.QFont()
        font.setFamily("Courier")
        self.boardInfo.setFont(font)
        self.boardInfo.setReadOnly(True)
        self.boardInfo.setObjectName("boardInfo")
        self.verticalLayout.addWidget(self.boardInfo)

        self.retranslateUi(DeviceStatus)
        QtCore.QMetaObject.connectSlotsByName(DeviceStatus)

    def retranslateUi(self, DeviceStatus):
        _translate = QtCore.QCoreApplication.translate
        DeviceStatus.setWindowTitle(_translate("DeviceStatus", "Form"))
        self.label_board.setText(_translate("DeviceStatus", "Board:"))
        self.sampleRate.setText(_translate("DeviceStatus", "0"))
        self.label_hz.setText(_translate("DeviceStatus", "Hz"))

from .measurement_status_indicator import MeasurementStatusIndicator
