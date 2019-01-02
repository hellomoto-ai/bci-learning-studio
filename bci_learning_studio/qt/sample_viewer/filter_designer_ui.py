# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './bci_learning_studio/qt/sample_viewer/filter_designer_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_filterDesigner(object):
    def setupUi(self, filterDesigner):
        filterDesigner.setObjectName("filterDesigner")
        filterDesigner.resize(679, 489)
        self.verticalLayout = QtWidgets.QVBoxLayout(filterDesigner)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.bandTypeSelector = QtWidgets.QComboBox(filterDesigner)
        self.bandTypeSelector.setObjectName("bandTypeSelector")
        self.horizontalLayout.addWidget(self.bandTypeSelector)
        self.label_filterFreq = QtWidgets.QLabel(filterDesigner)
        self.label_filterFreq.setObjectName("label_filterFreq")
        self.horizontalLayout.addWidget(self.label_filterFreq)
        self.criticalFreq = QtWidgets.QDoubleSpinBox(filterDesigner)
        self.criticalFreq.setMaximum(100000.0)
        self.criticalFreq.setObjectName("criticalFreq")
        self.horizontalLayout.addWidget(self.criticalFreq)
        self.label_bandwidth = QtWidgets.QLabel(filterDesigner)
        self.label_bandwidth.setObjectName("label_bandwidth")
        self.horizontalLayout.addWidget(self.label_bandwidth)
        self.bandWidth = QtWidgets.QDoubleSpinBox(filterDesigner)
        self.bandWidth.setObjectName("bandWidth")
        self.horizontalLayout.addWidget(self.bandWidth)
        self.label_order = QtWidgets.QLabel(filterDesigner)
        self.label_order.setObjectName("label_order")
        self.horizontalLayout.addWidget(self.label_order)
        self.filterOrder = QtWidgets.QSpinBox(filterDesigner)
        self.filterOrder.setObjectName("filterOrder")
        self.horizontalLayout.addWidget(self.filterOrder)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.plotter = PlotWidget(filterDesigner)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotter.sizePolicy().hasHeightForWidth())
        self.plotter.setSizePolicy(sizePolicy)
        self.plotter.setObjectName("plotter")
        self.verticalLayout.addWidget(self.plotter)
        self.buttonBox = QtWidgets.QDialogButtonBox(filterDesigner)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(filterDesigner)
        self.buttonBox.accepted.connect(filterDesigner.accept)
        self.buttonBox.rejected.connect(filterDesigner.reject)
        QtCore.QMetaObject.connectSlotsByName(filterDesigner)

    def retranslateUi(self, filterDesigner):
        _translate = QtCore.QCoreApplication.translate
        filterDesigner.setWindowTitle(_translate("filterDesigner", "Dialog"))
        self.label_filterFreq.setText(_translate("filterDesigner", "Filter Freq"))
        self.label_bandwidth.setText(_translate("filterDesigner", "Bandwidth"))
        self.label_order.setText(_translate("filterDesigner", "Order"))

from pyqtgraph import PlotWidget
