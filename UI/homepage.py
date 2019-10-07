# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'homepage.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1213, 662)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1301, 81))
        self.widget.setStyleSheet("background-color:rgb(43, 86, 190)")
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(30, 10, 65, 60))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../venv/images/DeepinScreenshot_20190821152323-removebg-preview.png"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(110, 20, 121, 41))
        self.label_2.setObjectName("label_2")
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setGeometry(QtCore.QRect(20, 100, 241, 601))
        self.widget_2.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.widget_2.setObjectName("widget_2")
        self.label_3 = QtWidgets.QLabel(self.widget_2)
        self.label_3.setGeometry(QtCore.QRect(70, 40, 101, 101))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("images/17004.svg"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.widget_2)
        self.label_4.setGeometry(QtCore.QRect(50, 160, 153, 32))
        self.label_4.setScaledContents(False)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.widget_2)
        self.label_5.setGeometry(QtCore.QRect(50, 210, 71, 17))
        self.label_5.setObjectName("label_5")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(730, 130, 131, 41))
        self.pushButton.setStyleSheet("background-color: rgb(43, 86, 190)")
        self.pushButton.setObjectName("pushButton")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(670, 120, 41, 51))
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
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:26pt; font-weight:600; color:#ffffff;\">DocAid</span></p></body></html>"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:20pt;\">Rohit Nagraj</span></p></body></html>"))
        self.label_5.setText(_translate("MainWindow", "Gender: M"))
        self.pushButton.setText(_translate("MainWindow", "Start Listening"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
