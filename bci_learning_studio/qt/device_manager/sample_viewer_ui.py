# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './bci_learning_studio/qt/device_manager/sample_plotter_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SampleViewer(object):
    def setupUi(self, SampleViewer):
        SampleViewer.setObjectName("SampleViewer")
        SampleViewer.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(SampleViewer)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.viewer = ViewerWidget(self.centralwidget)
        self.viewer.setObjectName("viewer")
        self.gridLayout.addWidget(self.viewer, 0, 0, 1, 1)
        SampleViewer.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(SampleViewer)
        self.statusbar.setObjectName("statusbar")
        SampleViewer.setStatusBar(self.statusbar)

        self.retranslateUi(SampleViewer)
        QtCore.QMetaObject.connectSlotsByName(SampleViewer)

    def retranslateUi(self, SampleViewer):
        _translate = QtCore.QCoreApplication.translate
        SampleViewer.setWindowTitle(_translate("SampleViewer", "Plot"))

from bci_learning_studio.qt.sample_viewer.viewer import ViewerWidget
