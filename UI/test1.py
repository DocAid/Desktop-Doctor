# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
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
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(240, 180, 343, 161))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setMaximumSize(QtCore.QSize(65, 60))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../venv/images/DeepinScreenshot_20190821152323-removebg-preview.png"))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setMaximumSize(QtCore.QSize(293, 32))
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setMaximumSize(QtCore.QSize(341, 24))
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        DocAid.setCentralWidget(self.centralwidget)

        self.retranslateUi(DocAid)
        QtCore.QMetaObject.connectSlotsByName(DocAid)

    def retranslateUi(self, DocAid):
        _translate = QtCore.QCoreApplication.translate
        DocAid.setWindowTitle(_translate("DocAid", "MainWindow"))
        self.label_2.setText(_translate("DocAid", "<html><head/><body><p><span style=\" font-size:20pt; font-weight:600;\">WELCOME TO DOCAID</span></p></body></html>"))
        self.pushButton.setText(_translate("DocAid", "Next"))
        self.label_3.setText(_translate("DocAid", "<html><head/><body><p><span style=\" font-size:16pt;\">Ask the patient to scan the QR code</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication(sys.argv)
    DocAid = QtWidgets.QMainWindow()
    ui = Ui_DocAid()
    ui.setupUi(DocAid)
    DocAid.show()
    sys.exit(app.exec_())
