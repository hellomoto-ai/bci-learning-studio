# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './bci_learning_studio/session/cursor_control/mode_selector_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ModeSelector(object):
    def setupUi(self, ModeSelector):
        ModeSelector.setObjectName("ModeSelector")
        ModeSelector.resize(337, 149)
        font = QtGui.QFont()
        font.setPointSize(13)
        ModeSelector.setFont(font)
        ModeSelector.setLayoutDirection(QtCore.Qt.LeftToRight)
        ModeSelector.setIconSize(QtCore.QSize(32, 32))
        ModeSelector.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.centralwidget = QtWidgets.QWidget(ModeSelector)
        self.centralwidget.setObjectName("centralwidget")
        ModeSelector.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar(ModeSelector)
        self.toolBar.setMovable(False)
        self.toolBar.setObjectName("toolBar")
        ModeSelector.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionRecord = QtWidgets.QAction(ModeSelector)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/resource/baseline-games-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRecord.setIcon(icon)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.actionRecord.setFont(font)
        self.actionRecord.setObjectName("actionRecord")
        self.actionEdit = QtWidgets.QAction(ModeSelector)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/resource/baseline-edit-24px.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEdit.setIcon(icon1)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.actionEdit.setFont(font)
        self.actionEdit.setObjectName("actionEdit")
        self.toolBar.addAction(self.actionRecord)
        self.toolBar.addAction(self.actionEdit)

        self.retranslateUi(ModeSelector)
        QtCore.QMetaObject.connectSlotsByName(ModeSelector)

    def retranslateUi(self, ModeSelector):
        _translate = QtCore.QCoreApplication.translate
        ModeSelector.setWindowTitle(_translate("ModeSelector", "MainWindow"))
        self.toolBar.setWindowTitle(_translate("ModeSelector", "toolBar"))
        self.actionRecord.setText(_translate("ModeSelector", "Record"))
        self.actionEdit.setText(_translate("ModeSelector", "Edit"))

import bci_learning_studio.qt.resource_rc
