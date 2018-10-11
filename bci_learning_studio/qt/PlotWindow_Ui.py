# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './bci_learning_studio/qt/PlotWindow_Ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Plot(object):
    def setupUi(self, Plot):
        Plot.setObjectName("Plot")
        Plot.resize(688, 608)
        self.centralwidget = QtWidgets.QWidget(Plot)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.plotWidget = PlotWidget(self.centralwidget)
        self.plotWidget.setObjectName("plotWidget")
        self.gridLayout.addWidget(self.plotWidget, 0, 0, 1, 1)
        Plot.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Plot)
        self.statusbar.setObjectName("statusbar")
        Plot.setStatusBar(self.statusbar)

        self.retranslateUi(Plot)
        QtCore.QMetaObject.connectSlotsByName(Plot)

    def retranslateUi(self, Plot):
        _translate = QtCore.QCoreApplication.translate
        Plot.setWindowTitle(_translate("Plot", "Plot"))

from bci_learning_studio.qt.PlotWidget import PlotWidget
