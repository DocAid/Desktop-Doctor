# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'opening.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Ui_DocAid(object):
    def setupUi(self, DocAid):
        DocAid.setObjectName("DocAid")
        DocAid.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(DocAid)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(370, 180, 65, 60))
        self.label.setMaximumSize(QtCore.QSize(65, 60))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../venv/images/DeepinScreenshot_20190821152323-removebg-preview.png"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(262, 260, 293, 32))
        self.label_2.setMaximumSize(QtCore.QSize(293, 32))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(240, 300, 341, 24))
        self.label_3.setMaximumSize(QtCore.QSize(341, 24))
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(370, 370, 89, 25))
        self.pushButton.setObjectName("pushButton")
        DocAid.setCentralWidget(self.centralwidget)

        self.retranslateUi(DocAid)
        QtCore.QMetaObject.connectSlotsByName(DocAid)

    def retranslateUi(self, DocAid):
        _translate = QtCore.QCoreApplication.translate
        DocAid.setWindowTitle(_translate("DocAid", "MainWindow"))
        self.label_2.setText(_translate("DocAid", "<html><head/><body><p><span style=\" font-size:20pt; font-weight:600;\">WELCOME TO DOCAID</span></p></body></html>"))
        self.label_3.setText(_translate("DocAid", "<html><head/><body><p><span style=\" font-size:16pt;\">Ask the patient to scan the QR code</span></p></body></html>"))
        self.pushButton.setText(_translate("DocAid", "Next"))
        # self.pushButton.clicked.connect(self.goHomepage)

    def goHomepage(self):
        # self.homepage= Ui_MainWindow()
        # self.setWindowTitle("Homapage")
        # self.setCentralWidget(self.Window)
        # self.show()
        # self.homepage.show()
        Homepage = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(Homepage)
        # Homapage.show()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 800, 71))
        self.widget.setStyleSheet("background-color:rgb(43, 86, 190)")
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(30, 4, 65, 60))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../venv/images/DeepinScreenshot_20190821152323-removebg-preview.png"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(110, 15, 121, 41))
        self.label_2.setObjectName("label_2")
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setGeometry(QtCore.QRect(19, 99, 211, 471))
        self.widget_2.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.widget_2.setObjectName("widget_2")
        self.label_3 = QtWidgets.QLabel(self.widget_2)
        self.label_3.setGeometry(QtCore.QRect(50, 30, 101, 101))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("images/17004.svg"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.widget_2)
        self.label_4.setGeometry(QtCore.QRect(30, 150, 153, 32))
        self.label_4.setScaledContents(False)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.widget_2)
        self.label_5.setGeometry(QtCore.QRect(30, 200, 71, 17))
        self.label_5.setObjectName("label_5")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(520, 120, 131, 41))
        self.pushButton.setStyleSheet("background-color: rgb(43, 86, 190)")
        self.pushButton.setObjectName("pushButton")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(460, 110, 41, 51))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("images/microphone-solid.svg"))
        self.label_6.setScaledContents(True)
        self.label_6.setObjectName("label_6")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:22pt; font-weight:600; color:#ffffff;\">DocAid</span></p></body></html>"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:20pt;\">Rohit Nagraj</span></p></body></html>"))
        self.label_5.setText(_translate("MainWindow", "Gender: M"))
        self.pushButton.setText(_translate("MainWindow", "Start Listening"))

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.docAid = Ui_DocAid()
        self.homepage = Ui_MainWindow()
        self.startUIWindow()

    def startUIWindow(self):
        self.docAid.setupUi(self)
        self.docAid.pushButton.clicked.connect(self.goHomepage)
        # self.uiToolTab.CPSBTN.clicked.connect(self.startUIWindow)
        self.show()

    def goHomepage(self):
        self.homepage.setupUi(self)
        # self.uiWindow.ToolsBTN.clicked.connect(self.startUIToolTab)
        self.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    # DocAid = QtWidgets.QMainWindow()
    # ui = Ui_DocAid()
    # ui.setupUi(DocAid)
    # DocAid.show()
    sys.exit(app.exec_())
