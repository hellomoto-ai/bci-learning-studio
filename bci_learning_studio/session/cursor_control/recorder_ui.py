# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './bci_learning_studio/session/cursor_control/recorder_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Recorder(object):
    def setupUi(self, Recorder):
        Recorder.setObjectName("Recorder")
        Recorder.resize(555, 604)
        self.centralwidget = QtWidgets.QWidget(Recorder)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.cursorControl = CursorControl(self.centralwidget)
        self.cursorControl.setStyleSheet("background-color:rgb(255, 255, 255);border:1px solid rgb(00, 00, 00);")
        self.cursorControl.setObjectName("cursorControl")
        self.verticalLayout.addWidget(self.cursorControl)
        Recorder.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Recorder)
        self.statusbar.setObjectName("statusbar")
        Recorder.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(Recorder)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName("toolBar")
        Recorder.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionRecord = QtWidgets.QAction(Recorder)
        self.actionRecord.setCheckable(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/resource/baseline-fiber_manual_record-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/icon/resource/baseline-stop-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionRecord.setIcon(icon)
        self.actionRecord.setObjectName("actionRecord")
        self.actionSave = QtWidgets.QAction(Recorder)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/resource/baseline-save-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon1)
        self.actionSave.setObjectName("actionSave")
        self.actionDevice = QtWidgets.QAction(Recorder)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/resource/baseline-developer_board-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDevice.setIcon(icon2)
        self.actionDevice.setObjectName("actionDevice")
        self.actionPlot = QtWidgets.QAction(Recorder)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icon/resource/baseline-show_chart-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPlot.setIcon(icon3)
        self.actionPlot.setObjectName("actionPlot")
        self.actionStart = QtWidgets.QAction(Recorder)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icon/resource/baseline-games-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionStart.setIcon(icon4)
        self.actionStart.setObjectName("actionStart")
        self.toolBar.addAction(self.actionRecord)
        self.toolBar.addAction(self.actionStart)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionDevice)

        self.retranslateUi(Recorder)
        QtCore.QMetaObject.connectSlotsByName(Recorder)

    def retranslateUi(self, Recorder):
        _translate = QtCore.QCoreApplication.translate
        Recorder.setWindowTitle(_translate("Recorder", "Recorder"))
        self.toolBar.setWindowTitle(_translate("Recorder", "toolBar"))
        self.actionRecord.setText(_translate("Recorder", "Record"))
        self.actionSave.setText(_translate("Recorder", "Save"))
        self.actionSave.setShortcut(_translate("Recorder", "Ctrl+S"))
        self.actionDevice.setText(_translate("Recorder", "Device"))
        self.actionPlot.setText(_translate("Recorder", "Plot"))
        self.actionStart.setText(_translate("Recorder", "Start"))

from .cursor_control import CursorControl
import bci_learning_studio.qt.resource_rc
