# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './bci_learning_studio/session/cursor_control/main_window_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(555, 604)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.cursorControl = CursorControl(self.centralwidget)
        self.cursorControl.setStyleSheet("background-color:rgb(255, 255, 255);border:1px solid rgb(00, 00, 00);")
        self.cursorControl.setObjectName("cursorControl")
        self.verticalLayout.addWidget(self.cursorControl)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionStart = QtWidgets.QAction(MainWindow)
        self.actionStart.setCheckable(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/resource/baseline-fiber_manual_record-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/icon/resource/baseline-stop-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionStart.setIcon(icon)
        self.actionStart.setObjectName("actionStart")
        self.actionSave = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/resource/baseline-save-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon1)
        self.actionSave.setObjectName("actionSave")
        self.actionDevice = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/resource/baseline-developer_board-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDevice.setIcon(icon2)
        self.actionDevice.setObjectName("actionDevice")
        self.actionPlot = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icon/resource/baseline-show_chart-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPlot.setIcon(icon3)
        self.actionPlot.setObjectName("actionPlot")
        self.toolBar.addAction(self.actionStart)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionDevice)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionStart.setText(_translate("MainWindow", "Start"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionDevice.setText(_translate("MainWindow", "Device"))
        self.actionPlot.setText(_translate("MainWindow", "Plot"))

from .cursor_control import CursorControl
import bci_learning_studio.qt.resource_rc
