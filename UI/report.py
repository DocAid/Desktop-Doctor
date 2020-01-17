# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'report.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Report(object):
    def setupUi(self, Report):
        Report.setObjectName("Report")
        Report.resize(1213, 662)
        self.centralwidget = QtWidgets.QWidget(Report)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1231, 81))
        self.widget.setStyleSheet("background-color:rgb(43, 86, 190)")
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(30, 8, 65, 60))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../venv/images/DeepinScreenshot_20190821152323-removebg-preview.png"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(110, 18, 121, 41))
        self.label_2.setObjectName("label_2")
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setGeometry(QtCore.QRect(20, 110, 241, 511))
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
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setGeometry(QtCore.QRect(300, 110, 881, 101))
        self.widget_3.setStyleSheet("background-color:rgb(43, 86, 190)")
        self.widget_3.setObjectName("widget_3")
        self.label_6 = QtWidgets.QLabel(self.widget_3)
        self.label_6.setGeometry(QtCore.QRect(40, 40, 401, 28))
        self.label_6.setObjectName("label_6")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(1040, 590, 131, 41))
        self.pushButton.setStyleSheet("background-color:rgb(43, 86, 190);color:rgb(255, 255, 255)")
        self.pushButton.setObjectName("pushButton")
        self.pres = QtWidgets.QLabel(self.centralwidget)
        self.pres.setGeometry(QtCore.QRect(310, 240, 861, 321))
        self.pres.setText("")
        self.pres.setObjectName("pres")
        Report.setCentralWidget(self.centralwidget)

        self.retranslateUi(Report)
        QtCore.QMetaObject.connectSlotsByName(Report)

    def retranslateUi(self, Report):
        _translate = QtCore.QCoreApplication.translate
        Report.setWindowTitle(_translate("Report", "MainWindow"))
        self.label_2.setText(_translate("Report", "<html><head/><body><p><span style=\" font-size:22pt; font-weight:600; color:#ffffff;\">DocAid</span></p></body></html>"))
        self.label_4.setText(_translate("Report", "<html><head/><body><p><span style=\" font-size:20pt;\">Rohit Nagraj</span></p></body></html>"))
        self.label_6.setText(_translate("Report", "<html><head/><body><p><span style=\" font-size:18pt; color:#ffffff;\">Prescription for Fever</span></p></body></html>"))
        self.pushButton.setText(_translate("Report", "Generate PDF"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Report = QtWidgets.QMainWindow()
    ui = Ui_Report()
    ui.setupUi(Report)
    Report.show()
    sys.exit(app.exec_())
