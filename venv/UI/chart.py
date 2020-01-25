# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chart.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication)
import requests as rq
import urllib.request


class Ui_chart(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 391, 291))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(420, 10, 361, 291))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 300, 401, 251))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(430, 300, 351, 251))
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        hbox = QHBoxLayout()
        URL="http://6bf7636e.ngrok.io/docChart1"
        r=rq.get(url=URL)
        data=r.json()
        print(data)
        self.label.setText(_translate("MainWindow", "Image1"))
        print(data['chart_url'])
        newdat = urllib.request.urlopen(data['chart_url']).read()
        print(newdat)
        img = QtGui.QImage()
        print(img)
        img.loadFromData(newdat)
        img = img.scaled(380, 380, QtCore.Qt.KeepAspectRatio)
        print(img)
        self.label.setPixmap(QtGui.QPixmap(img))
        URL1 = "http://6bf7636e.ngrok.io/docChart2"
        self.label_2.setText(_translate("MainWindow", "Image2"))
        r1 = rq.get(url=URL1)
        data1 = r1.json()
        print(data1)
        print(data1['chart_url'])
        newdat = urllib.request.urlopen(data1['chart_url']).read()
        print(newdat)
        img = QtGui.QImage()
        print(img)
        img.loadFromData(newdat)
        img = img.scaled(380, 380, QtCore.Qt.KeepAspectRatio)
        print(img)
        self.label_2.setPixmap(QtGui.QPixmap(img))
        self.label_3.setText(_translate("MainWindow", "Image3"))
        URL2 = "http://6bf7636e.ngrok.io/docChart3"
        r2 = rq.get(url=URL2)
        data2 = r2.json()
        print(data2)
        print(data2['chart_url'])
        newdat = urllib.request.urlopen(data2['chart_url']).read()
        print(newdat)
        img = QtGui.QImage()
        print(img)
        img.loadFromData(newdat)
        img = img.scaled(380, 380, QtCore.Qt.KeepAspectRatio)
        print(img)
        self.label_3.setPixmap(QtGui.QPixmap(img))
        self.label_4.setText(_translate("MainWindow", "Image4"))
        URL3 = "http://6bf7636e.ngrok.io/docChart4"
        r3 = rq.get(url=URL3)
        data3 = r3.json()
        print(data3)
        print(data3['chart_url'])
        newdat = urllib.request.urlopen(data3['chart_url']).read()
        print(newdat)
        img = QtGui.QImage()
        print(img)
        img.loadFromData(newdat)
        img = img.scaled(380, 380, QtCore.Qt.KeepAspectRatio)
        print(img)
        self.label_4.setPixmap(QtGui.QPixmap(img))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DocAid = QtWidgets.QMainWindow()
    ui = Ui_chart()
    ui.setupUi(DocAid)
    DocAid.show()
    sys.exit(app.exec_())
