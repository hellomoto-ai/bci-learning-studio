# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './bci_learning_studio/qt/cyton_configuration_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CytonConfiguration(object):
    def setupUi(self, CytonConfiguration):
        CytonConfiguration.setObjectName("CytonConfiguration")
        CytonConfiguration.resize(762, 500)
        self.centralwidget = QtWidgets.QWidget(CytonConfiguration)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.boardConfig_Label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.boardConfig_Label.setFont(font)
        self.boardConfig_Label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.boardConfig_Label.setObjectName("boardConfig_Label")
        self.verticalLayout.addWidget(self.boardConfig_Label)
        self.boardMode_Layout = QtWidgets.QHBoxLayout()
        self.boardMode_Layout.setObjectName("boardMode_Layout")
        self.boadMode_Label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.boadMode_Label.sizePolicy().hasHeightForWidth())
        self.boadMode_Label.setSizePolicy(sizePolicy)
        self.boadMode_Label.setObjectName("boadMode_Label")
        self.boardMode_Layout.addWidget(self.boadMode_Label)
        self.boardMode_ComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.boardMode_ComboBox.setObjectName("boardMode_ComboBox")
        self.boardMode_ComboBox.addItem("")
        self.boardMode_ComboBox.addItem("")
        self.boardMode_ComboBox.addItem("")
        self.boardMode_ComboBox.addItem("")
        self.boardMode_ComboBox.addItem("")
        self.boardMode_Layout.addWidget(self.boardMode_ComboBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.boardMode_Layout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.boardMode_Layout)
        self.sampleRate_Layout = QtWidgets.QHBoxLayout()
        self.sampleRate_Layout.setObjectName("sampleRate_Layout")
        self.sampleRate_Label = QtWidgets.QLabel(self.centralwidget)
        self.sampleRate_Label.setObjectName("sampleRate_Label")
        self.sampleRate_Layout.addWidget(self.sampleRate_Label)
        self.sampleRate_ComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.sampleRate_ComboBox.setObjectName("sampleRate_ComboBox")
        self.sampleRate_ComboBox.addItem("")
        self.sampleRate_ComboBox.addItem("")
        self.sampleRate_ComboBox.addItem("")
        self.sampleRate_ComboBox.addItem("")
        self.sampleRate_ComboBox.addItem("")
        self.sampleRate_ComboBox.addItem("")
        self.sampleRate_ComboBox.addItem("")
        self.sampleRate_Layout.addWidget(self.sampleRate_ComboBox)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.sampleRate_Layout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.sampleRate_Layout)
        self.channelConfig_Label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.channelConfig_Label.setFont(font)
        self.channelConfig_Label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.channelConfig_Label.setObjectName("channelConfig_Label")
        self.verticalLayout.addWidget(self.channelConfig_Label)
        self.channelConfig_Table = QtWidgets.QTableWidget(self.centralwidget)
        self.channelConfig_Table.setShowGrid(False)
        self.channelConfig_Table.setRowCount(8)
        self.channelConfig_Table.setColumnCount(7)
        self.channelConfig_Table.setObjectName("channelConfig_Table")
        self.verticalLayout.addWidget(self.channelConfig_Table)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        CytonConfiguration.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(CytonConfiguration)
        self.statusbar.setObjectName("statusbar")
        CytonConfiguration.setStatusBar(self.statusbar)

        self.retranslateUi(CytonConfiguration)
        self.sampleRate_ComboBox.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(CytonConfiguration)

    def retranslateUi(self, CytonConfiguration):
        _translate = QtCore.QCoreApplication.translate
        CytonConfiguration.setWindowTitle(_translate("CytonConfiguration", "Cyton Configuration"))
        self.boardConfig_Label.setText(_translate("CytonConfiguration", "Board Configuration"))
        self.boadMode_Label.setText(_translate("CytonConfiguration", "Board Mode"))
        self.boardMode_ComboBox.setItemText(0, _translate("CytonConfiguration", "Default"))
        self.boardMode_ComboBox.setItemText(1, _translate("CytonConfiguration", "Debug"))
        self.boardMode_ComboBox.setItemText(2, _translate("CytonConfiguration", "Analog"))
        self.boardMode_ComboBox.setItemText(3, _translate("CytonConfiguration", "Digital"))
        self.boardMode_ComboBox.setItemText(4, _translate("CytonConfiguration", "Marker"))
        self.sampleRate_Label.setText(_translate("CytonConfiguration", "Sample Rate"))
        self.sampleRate_ComboBox.setItemText(0, _translate("CytonConfiguration", "250"))
        self.sampleRate_ComboBox.setItemText(1, _translate("CytonConfiguration", "500"))
        self.sampleRate_ComboBox.setItemText(2, _translate("CytonConfiguration", "1000"))
        self.sampleRate_ComboBox.setItemText(3, _translate("CytonConfiguration", "2000"))
        self.sampleRate_ComboBox.setItemText(4, _translate("CytonConfiguration", "4000"))
        self.sampleRate_ComboBox.setItemText(5, _translate("CytonConfiguration", "8000"))
        self.sampleRate_ComboBox.setItemText(6, _translate("CytonConfiguration", "16000"))
        self.channelConfig_Label.setText(_translate("CytonConfiguration", "Channel Configuration"))
