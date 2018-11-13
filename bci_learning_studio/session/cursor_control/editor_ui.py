# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './bci_learning_studio/session/cursor_control/editor_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Editor(object):
    def setupUi(self, Editor):
        Editor.setObjectName("Editor")
        Editor.resize(567, 564)
        self.widget = QtWidgets.QWidget(Editor)
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.cursorReplay = CursorReplay(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.cursorReplay.sizePolicy().hasHeightForWidth())
        self.cursorReplay.setSizePolicy(sizePolicy)
        self.cursorReplay.setMinimumSize(QtCore.QSize(100, 100))
        self.cursorReplay.setStyleSheet("")
        self.cursorReplay.setObjectName("cursorReplay")
        self.verticalLayout.addWidget(self.cursorReplay)
        self.line = QtWidgets.QFrame(self.widget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.graphWidget = GraphicsLayoutWidget(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.graphWidget.sizePolicy().hasHeightForWidth())
        self.graphWidget.setSizePolicy(sizePolicy)
        self.graphWidget.setObjectName("graphWidget")
        self.verticalLayout.addWidget(self.graphWidget)
        self.gridLayout.addLayout(self.verticalLayout, 1, 1, 1, 1)
        Editor.setCentralWidget(self.widget)
        self.menubar = QtWidgets.QMenuBar(Editor)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 567, 22))
        self.menubar.setNativeMenuBar(False)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        Editor.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Editor)
        self.statusbar.setObjectName("statusbar")
        Editor.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(Editor)
        self.actionOpen.setObjectName("actionOpen")
        self.menuFile.addAction(self.actionOpen)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(Editor)
        QtCore.QMetaObject.connectSlotsByName(Editor)

    def retranslateUi(self, Editor):
        _translate = QtCore.QCoreApplication.translate
        Editor.setWindowTitle(_translate("Editor", "Editor"))
        self.menuFile.setTitle(_translate("Editor", "File"))
        self.actionOpen.setText(_translate("Editor", "Open"))
        self.actionOpen.setShortcut(_translate("Editor", "Ctrl+O"))

from .cursor_replay import CursorReplay
from pyqtgraph import GraphicsLayoutWidget
