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
        Editor.resize(600, 600)
        self.widget = QtWidgets.QWidget(Editor)
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")
        self.cursorReplay = CursorReplay(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.cursorReplay.sizePolicy().hasHeightForWidth())
        self.cursorReplay.setSizePolicy(sizePolicy)
        self.cursorReplay.setMinimumSize(QtCore.QSize(100, 100))
        self.cursorReplay.setStyleSheet("")
        self.cursorReplay.setObjectName("cursorReplay")
        self.gridLayout.addWidget(self.cursorReplay, 0, 1, 1, 1)
        Editor.setCentralWidget(self.widget)
        self.menubar = QtWidgets.QMenuBar(Editor)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 22))
        self.menubar.setNativeMenuBar(False)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        Editor.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Editor)
        self.statusbar.setObjectName("statusbar")
        Editor.setStatusBar(self.statusbar)
        self.dockWidget = QtWidgets.QDockWidget(Editor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidget.sizePolicy().hasHeightForWidth())
        self.dockWidget.setSizePolicy(sizePolicy)
        self.dockWidget.setMinimumSize(QtCore.QSize(400, 322))
        self.dockWidget.setObjectName("dockWidget")
        self.viewer = ViewerWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.viewer.sizePolicy().hasHeightForWidth())
        self.viewer.setSizePolicy(sizePolicy)
        self.viewer.setMinimumSize(QtCore.QSize(400, 300))
        self.viewer.setObjectName("viewer")
        self.dockWidget.setWidget(self.viewer)
        Editor.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidget)
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
from bci_learning_studio.qt.sample_viewer.viewer_widget import ViewerWidget
