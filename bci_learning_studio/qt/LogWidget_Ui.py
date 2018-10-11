# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './bci_learning_studio/qt/LogWidget_Ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LogWidget(object):
    def setupUi(self, LogWidget):
        LogWidget.setObjectName("LogWidget")
        LogWidget.resize(697, 564)
        self.verticalLayout = QtWidgets.QVBoxLayout(LogWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBoxFilter = QtWidgets.QComboBox(LogWidget)
        self.comboBoxFilter.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.comboBoxFilter.setObjectName("comboBoxFilter")
        self.horizontalLayout.addWidget(self.comboBoxFilter)
        self.pushButtonSave = QtWidgets.QPushButton(LogWidget)
        self.pushButtonSave.setObjectName("pushButtonSave")
        self.horizontalLayout.addWidget(self.pushButtonSave)
        self.pushButtonClear = QtWidgets.QPushButton(LogWidget)
        self.pushButtonClear.setObjectName("pushButtonClear")
        self.horizontalLayout.addWidget(self.pushButtonClear)
        spacerItem = QtWidgets.QSpacerItem(670, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textEditLog = QtWidgets.QTextEdit(LogWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEditLog.sizePolicy().hasHeightForWidth())
        self.textEditLog.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Courier")
        self.textEditLog.setFont(font)
        self.textEditLog.setObjectName("textEditLog")
        self.verticalLayout.addWidget(self.textEditLog)

        self.retranslateUi(LogWidget)
        QtCore.QMetaObject.connectSlotsByName(LogWidget)

    def retranslateUi(self, LogWidget):
        _translate = QtCore.QCoreApplication.translate
        LogWidget.setWindowTitle(_translate("LogWidget", "Log"))
        self.pushButtonSave.setText(_translate("LogWidget", "Save"))
        self.pushButtonClear.setText(_translate("LogWidget", "Clear"))

