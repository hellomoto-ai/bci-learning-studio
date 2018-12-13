# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './bci_learning_studio/qt/device_manager/log_widget_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LogWidget(object):
    def setupUi(self, LogWidget):
        LogWidget.setObjectName("LogWidget")
        LogWidget.resize(586, 395)
        self.verticalLayout = QtWidgets.QVBoxLayout(LogWidget)
        self.verticalLayout.setContentsMargins(-1, 0, -1, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.levelBox = QtWidgets.QComboBox(LogWidget)
        self.levelBox.setObjectName("levelBox")
        self.levelBox.addItem("")
        self.levelBox.addItem("")
        self.levelBox.addItem("")
        self.levelBox.addItem("")
        self.levelBox.addItem("")
        self.horizontalLayout.addWidget(self.levelBox)
        self.clearButton = QtWidgets.QPushButton(LogWidget)
        self.clearButton.setObjectName("clearButton")
        self.horizontalLayout.addWidget(self.clearButton)
        self.saveButton = QtWidgets.QPushButton(LogWidget)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout.addWidget(self.saveButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textEdit = QtWidgets.QTextEdit(LogWidget)
        font = QtGui.QFont()
        font.setFamily("Courier")
        self.textEdit.setFont(font)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)

        self.retranslateUi(LogWidget)
        QtCore.QMetaObject.connectSlotsByName(LogWidget)

    def retranslateUi(self, LogWidget):
        _translate = QtCore.QCoreApplication.translate
        LogWidget.setWindowTitle(_translate("LogWidget", "Form"))
        self.levelBox.setCurrentText(_translate("LogWidget", "INFO"))
        self.levelBox.setItemText(0, _translate("LogWidget", "DEBUG"))
        self.levelBox.setItemText(1, _translate("LogWidget", "INFO"))
        self.levelBox.setItemText(2, _translate("LogWidget", "WARNING"))
        self.levelBox.setItemText(3, _translate("LogWidget", "ERROR"))
        self.levelBox.setItemText(4, _translate("LogWidget", "CRITICAL"))
        self.clearButton.setText(_translate("LogWidget", "Clear"))
        self.saveButton.setText(_translate("LogWidget", "Save"))

