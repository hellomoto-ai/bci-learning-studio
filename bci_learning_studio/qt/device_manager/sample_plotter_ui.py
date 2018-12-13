# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './bci_learning_studio/qt/device_manager/sample_plotter_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SamplePlotter(object):
    def setupUi(self, SamplePlotter):
        SamplePlotter.setObjectName("SamplePlotter")
        SamplePlotter.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(SamplePlotter)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.graphWidget = GraphicsLayoutWidget(self.centralwidget)
        self.graphWidget.setObjectName("graphWidget")
        self.gridLayout.addWidget(self.graphWidget, 0, 0, 1, 1)
        SamplePlotter.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(SamplePlotter)
        self.statusbar.setObjectName("statusbar")
        SamplePlotter.setStatusBar(self.statusbar)

        self.retranslateUi(SamplePlotter)
        QtCore.QMetaObject.connectSlotsByName(SamplePlotter)

    def retranslateUi(self, SamplePlotter):
        _translate = QtCore.QCoreApplication.translate
        SamplePlotter.setWindowTitle(_translate("SamplePlotter", "Plot"))

from pyqtgraph import GraphicsLayoutWidget
