# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './bci_learning_studio/qt/sample_viewer/viewer_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_viewer(object):
    def setupUi(self, viewer):
        viewer.setObjectName("viewer")
        viewer.resize(618, 441)
        self.verticalLayout = QtWidgets.QVBoxLayout(viewer)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.configureFilter = QtWidgets.QPushButton(viewer)
        self.configureFilter.setObjectName("configureFilter")
        self.horizontalLayout.addWidget(self.configureFilter)
        self.clearFilter = QtWidgets.QPushButton(viewer)
        self.clearFilter.setObjectName("clearFilter")
        self.horizontalLayout.addWidget(self.clearFilter)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.plotter = GraphicsView(viewer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotter.sizePolicy().hasHeightForWidth())
        self.plotter.setSizePolicy(sizePolicy)
        self.plotter.setObjectName("plotter")
        self.verticalLayout.addWidget(self.plotter)

        self.retranslateUi(viewer)
        QtCore.QMetaObject.connectSlotsByName(viewer)

    def retranslateUi(self, viewer):
        _translate = QtCore.QCoreApplication.translate
        viewer.setWindowTitle(_translate("viewer", "Form"))
        self.configureFilter.setText(_translate("viewer", "Configure Filter"))
        self.clearFilter.setText(_translate("viewer", "Clear Filter"))

from pyqtgraph import GraphicsView
