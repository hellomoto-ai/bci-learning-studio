# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './debug/test_vispy/viewer_widget_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ViewerWidget(object):
    def setupUi(self, ViewerWidget):
        ViewerWidget.setObjectName("ViewerWidget")
        ViewerWidget.resize(618, 441)
        self.verticalLayout = QtWidgets.QVBoxLayout(ViewerWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.configureFilter = QtWidgets.QPushButton(ViewerWidget)
        self.configureFilter.setObjectName("configureFilter")
        self.horizontalLayout.addWidget(self.configureFilter)
        self.clearFilter = QtWidgets.QPushButton(ViewerWidget)
        self.clearFilter.setObjectName("clearFilter")
        self.horizontalLayout.addWidget(self.clearFilter)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.plotter = PlotterWidget(ViewerWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotter.sizePolicy().hasHeightForWidth())
        self.plotter.setSizePolicy(sizePolicy)
        self.plotter.setObjectName("plotter")
        self.verticalLayout.addWidget(self.plotter)

        self.retranslateUi(ViewerWidget)
        QtCore.QMetaObject.connectSlotsByName(ViewerWidget)

    def retranslateUi(self, ViewerWidget):
        _translate = QtCore.QCoreApplication.translate
        ViewerWidget.setWindowTitle(_translate("ViewerWidget", "Form"))
        self.configureFilter.setText(_translate("ViewerWidget", "Configure Filter"))
        self.clearFilter.setText(_translate("ViewerWidget", "Clear Filter"))

from bci_learning_studio.qt.sample_viewer.plotter_widget import PlotterWidget
