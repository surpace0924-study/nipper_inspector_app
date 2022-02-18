# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nipper_inspector.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(471, 137)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_LED1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_LED1.setGeometry(QtCore.QRect(10, 10, 101, 41))
        self.pushButton_LED1.setObjectName("pushButton_LED1")
        self.pushButton_LED2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_LED2.setGeometry(QtCore.QRect(120, 10, 101, 41))
        self.pushButton_LED2.setObjectName("pushButton_LED2")
        self.pushButton_LED3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_LED3.setGeometry(QtCore.QRect(230, 10, 101, 41))
        self.pushButton_LED3.setObjectName("pushButton_LED3")
        self.pushButton_LED4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_LED4.setGeometry(QtCore.QRect(340, 10, 101, 41))
        self.pushButton_LED4.setObjectName("pushButton_LED4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 471, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton_LED1.clicked.connect(MainWindow.button_generate_Click)
        self.pushButton_LED2.clicked.connect(MainWindow.button_speed_check)
        self.pushButton_LED3.clicked.connect(MainWindow.button_acceleration_check)
        self.pushButton_LED4.clicked.connect(MainWindow.button_curvature_check)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_LED1.setText(_translate("MainWindow", "LED1"))
        self.pushButton_LED2.setText(_translate("MainWindow", "LED2"))
        self.pushButton_LED3.setText(_translate("MainWindow", "LED3"))
        self.pushButton_LED4.setText(_translate("MainWindow", "LED4"))

