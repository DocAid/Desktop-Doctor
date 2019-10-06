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
        Report.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(Report)
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
        self.widget_2.setGeometry(QtCore.QRect(30, 100, 211, 471))
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
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setGeometry(QtCore.QRect(270, 100, 511, 80))
        self.widget_3.setStyleSheet("background-color:rgb(43, 86, 190)")
        self.widget_3.setObjectName("widget_3")
        self.label_6 = QtWidgets.QLabel(self.widget_3)
        self.label_6.setGeometry(QtCore.QRect(20, 20, 238, 28))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.widget_3)
        self.label_7.setGeometry(QtCore.QRect(30, 50, 94, 16))
        self.label_7.setObjectName("label_7")
        self.widget_4 = QtWidgets.QWidget(self.centralwidget)
        self.widget_4.setGeometry(QtCore.QRect(269, 219, 511, 91))
        self.widget_4.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.widget_4.setObjectName("widget_4")
        self.label_8 = QtWidgets.QLabel(self.widget_4)
        self.label_8.setGeometry(QtCore.QRect(20, 20, 183, 22))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.widget_4)
        self.label_9.setGeometry(QtCore.QRect(30, 53, 217, 17))
        self.label_9.setObjectName("label_9")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(640, 360, 121, 31))
        self.pushButton.setStyleSheet("background-color:rgb(43, 86, 190)")
        self.pushButton.setObjectName("pushButton")
        Report.setCentralWidget(self.centralwidget)

        self.retranslateUi(Report)
        QtCore.QMetaObject.connectSlotsByName(Report)

    def retranslateUi(self, Report):
        _translate = QtCore.QCoreApplication.translate
        Report.setWindowTitle(_translate("Report", "MainWindow"))
        self.label_2.setText(_translate("Report", "<html><head/><body><p><span style=\" font-size:22pt; font-weight:600; color:#ffffff;\">DocAid</span></p></body></html>"))
        self.label_4.setText(_translate("Report", "<html><head/><body><p><span style=\" font-size:20pt;\">Rohit Nagraj</span></p></body></html>"))
        self.label_5.setText(_translate("Report", "Gender: M"))
        self.label_6.setText(_translate("Report", "<html><head/><body><p><span style=\" font-size:18pt; color:#ffffff;\">Prescription for Fever</span></p></body></html>"))
        self.label_7.setText(_translate("Report", "<html><head/><body><p><span style=\" font-size:10pt; color:#ffffff;\">Visited on 3 Oct</span></p></body></html>"))
        self.label_8.setText(_translate("Report", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Paracetamol 500 mg</span></p></body></html>"))
        self.label_9.setText(_translate("Report", "2 tablets thrice a day for a week"))
        self.pushButton.setText(_translate("Report", "Generate PDF"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Report = QtWidgets.QMainWindow()
    ui = Ui_Report()
    ui.setupUi(Report)
    Report.show()
    sys.exit(app.exec_())
