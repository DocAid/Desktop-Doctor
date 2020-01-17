# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'opening.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DocAid(object):
    def setupUi(self, DocAid):
        DocAid.setObjectName("DocAid")
        DocAid.resize(1211, 662)
        self.centralwidget = QtWidgets.QWidget(DocAid)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(570, 200, 65, 60))
        self.label.setMaximumSize(QtCore.QSize(65, 60))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../venv/images/DeepinScreenshot_20190821152323-removebg-preview.png"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(462, 280, 293, 32))
        self.label_2.setMaximumSize(QtCore.QSize(293, 32))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(440, 320, 341, 24))
        self.label_3.setMaximumSize(QtCore.QSize(341, 24))
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(520, 370, 171, 41))
        self.pushButton.setStyleSheet("background-color:rgb(10, 62, 148);\n"
"color:rgb(255, 255, 255)")
        self.pushButton.setObjectName("pushButton")
        DocAid.setCentralWidget(self.centralwidget)

        self.retranslateUi(DocAid)
        QtCore.QMetaObject.connectSlotsByName(DocAid)

    def retranslateUi(self, DocAid):
        _translate = QtCore.QCoreApplication.translate
        DocAid.setWindowTitle(_translate("DocAid", "MainWindow"))
        self.label_2.setText(_translate("DocAid", "<html><head/><body><p><span style=\" font-size:19pt; font-weight:600;\">WELCOME TO DOCAID</span></p></body></html>"))
        self.label_3.setText(_translate("DocAid", "<html><head/><body><p><span style=\" font-size:16pt;\">Ask the patient to scan the QR code</span></p></body></html>"))
        self.pushButton.setText(_translate("DocAid", "Scan the QR"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DocAid = QtWidgets.QMainWindow()
    ui = Ui_DocAid()
    ui.setupUi(DocAid)
    DocAid.show()
    sys.exit(app.exec_())
