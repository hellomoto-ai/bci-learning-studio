# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './bci_learning_studio/qt/DeviceControllerWidget_Ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DeviceControllerWidget(object):
    def setupUi(self, DeviceControllerWidget):
        DeviceControllerWidget.setObjectName("DeviceControllerWidget")
        DeviceControllerWidget.resize(512, 363)
        self.verticalLayout = QtWidgets.QVBoxLayout(DeviceControllerWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButtonStreaming = QtWidgets.QPushButton(DeviceControllerWidget)
        self.pushButtonStreaming.setObjectName("pushButtonStreaming")
        self.horizontalLayout_3.addWidget(self.pushButtonStreaming)
        self.lineEditRate = QtWidgets.QLineEdit(DeviceControllerWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditRate.sizePolicy().hasHeightForWidth())
        self.lineEditRate.setSizePolicy(sizePolicy)
        self.lineEditRate.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lineEditRate.setAutoFillBackground(False)
        self.lineEditRate.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditRate.setReadOnly(True)
        self.lineEditRate.setObjectName("lineEditRate")
        self.horizontalLayout_3.addWidget(self.lineEditRate)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.pushButtonPlot = QtWidgets.QPushButton(DeviceControllerWidget)
        self.pushButtonPlot.setCheckable(True)
        self.pushButtonPlot.setObjectName("pushButtonPlot")
        self.horizontalLayout_3.addWidget(self.pushButtonPlot)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.textEditDeviceProertry = QtWidgets.QTextEdit(DeviceControllerWidget)
        self.textEditDeviceProertry.setReadOnly(True)
        self.textEditDeviceProertry.setObjectName("textEditDeviceProertry")
        self.verticalLayout.addWidget(self.textEditDeviceProertry)

        self.retranslateUi(DeviceControllerWidget)
        QtCore.QMetaObject.connectSlotsByName(DeviceControllerWidget)

    def retranslateUi(self, DeviceControllerWidget):
        _translate = QtCore.QCoreApplication.translate
        DeviceControllerWidget.setWindowTitle(_translate("DeviceControllerWidget", "Devece Controller"))
        self.pushButtonStreaming.setText(_translate("DeviceControllerWidget", "Start Streaming"))
        self.pushButtonPlot.setText(_translate("DeviceControllerWidget", "Plot"))

