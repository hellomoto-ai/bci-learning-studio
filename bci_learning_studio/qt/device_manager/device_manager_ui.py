# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './bci_learning_studio/qt/device_manager/device_manager_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DeviceManager(object):
    def setupUi(self, DeviceManager):
        DeviceManager.setObjectName("DeviceManager")
        DeviceManager.resize(577, 343)
        self.centralwidget = QtWidgets.QWidget(DeviceManager)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.deviceStatus = DeviceStatus(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.deviceStatus.sizePolicy().hasHeightForWidth())
        self.deviceStatus.setSizePolicy(sizePolicy)
        self.deviceStatus.setMaximumSize(QtCore.QSize(16777215, 150))
        self.deviceStatus.setObjectName("deviceStatus")
        self.verticalLayout.addWidget(self.deviceStatus)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.logWidget = LogWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.logWidget.sizePolicy().hasHeightForWidth())
        self.logWidget.setSizePolicy(sizePolicy)
        self.logWidget.setObjectName("logWidget")
        self.verticalLayout.addWidget(self.logWidget)
        DeviceManager.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(DeviceManager)
        self.statusbar.setObjectName("statusbar")
        DeviceManager.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(DeviceManager)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBar.sizePolicy().hasHeightForWidth())
        self.toolBar.setSizePolicy(sizePolicy)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName("toolBar")
        DeviceManager.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionConnect = QtWidgets.QAction(DeviceManager)
        self.actionConnect.setCheckable(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/resource/baseline-phonelink-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/icon/resource/baseline-phonelink_off-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionConnect.setIcon(icon)
        self.actionConnect.setObjectName("actionConnect")
        self.actionStream = QtWidgets.QAction(DeviceManager)
        self.actionStream.setCheckable(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/resource/baseline-play_arrow-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(":/icon/resource/baseline-stop-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionStream.setIcon(icon1)
        self.actionStream.setObjectName("actionStream")
        self.actionConfigure = QtWidgets.QAction(DeviceManager)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/resource/baseline-settings-20px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionConfigure.setIcon(icon2)
        self.actionConfigure.setObjectName("actionConfigure")
        self.actionPlot = QtWidgets.QAction(DeviceManager)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icon/resource/baseline-show_chart-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPlot.setIcon(icon3)
        self.actionPlot.setObjectName("actionPlot")
        self.toolBar.addAction(self.actionConnect)
        self.toolBar.addAction(self.actionStream)
        self.toolBar.addAction(self.actionConfigure)
        self.toolBar.addAction(self.actionPlot)

        self.retranslateUi(DeviceManager)
        QtCore.QMetaObject.connectSlotsByName(DeviceManager)

    def retranslateUi(self, DeviceManager):
        _translate = QtCore.QCoreApplication.translate
        DeviceManager.setWindowTitle(_translate("DeviceManager", "Device Manager"))
        self.toolBar.setWindowTitle(_translate("DeviceManager", "toolBar"))
        self.actionConnect.setText(_translate("DeviceManager", "Connect"))
        self.actionStream.setText(_translate("DeviceManager", "Stream"))
        self.actionConfigure.setText(_translate("DeviceManager", "Configure"))
        self.actionPlot.setText(_translate("DeviceManager", "Plot"))

from .device_status import DeviceStatus
from .log_widget import LogWidget
import bci_learning_studio.qt.resource_rc
