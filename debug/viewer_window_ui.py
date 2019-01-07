# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './debug/viewer_window_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ViewerWindow(object):
    def setupUi(self, ViewerWindow):
        ViewerWindow.setObjectName("ViewerWindow")
        ViewerWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(ViewerWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.sampleViewer = ViewerWidget(self.centralwidget)
        self.sampleViewer.setObjectName("sampleViewer")
        self.verticalLayout.addWidget(self.sampleViewer)
        ViewerWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ViewerWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        ViewerWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ViewerWindow)
        self.statusbar.setObjectName("statusbar")
        ViewerWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ViewerWindow)
        QtCore.QMetaObject.connectSlotsByName(ViewerWindow)

    def retranslateUi(self, ViewerWindow):
        _translate = QtCore.QCoreApplication.translate
        ViewerWindow.setWindowTitle(_translate("ViewerWindow", "MainWindow"))

from bci_learning_studio.qt.sample_viewer.viewer import ViewerWidget
