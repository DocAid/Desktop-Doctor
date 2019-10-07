from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import requests 
from opening import Ui_DocAid
from homepage import Ui_MainWindow
from prescription import Ui_Prescription
from report import Ui_Report
import json

QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.docAid = Ui_DocAid()
        self.homepage = Ui_MainWindow()
        self.prescription=Ui_Prescription()
        self.report=Ui_Report()
        self.startUIWindow()

    def startUIWindow(self):
        self.docAid.setupUi(self)
        self.docAid.pushButton.clicked.connect(self.goHomepage)
        self.show()

    def goHomepage(self):
        # self.docAid.pushButton.setText("Loading")
        self.homepage.setupUi(self)
        details=requests.get('https://uinames.com/api/?amount=1')
        details=json.loads(details.text)
        print(details["name"])
        self.homepage.label_4.setText(details["name"]+details["surname"])
        self.homepage.label_5.setText(details["gender"])
        self.homepage.pushButton.clicked.connect(self.goPrescription)
        self.show()
    
    def goPrescription(self):
        self.prescription.setupUi(self)
        self.prescription.pushButton_9.clicked.connect(self.goReport)
        self.show()

    def goReport(self):
        self.report.setupUi(self)
        details=requests.get('https://uinames.com/api/?amount=1')
        details=json.loads(details.text)
        print(details["name"])
        self.report.label_4.setText(details["name"]+details["surname"])
        self.report.label_5.setText(details["gender"])
        # self.homepage.pushButton.setText("Clicked")
        # self.prescription.setupUi(self)
        self.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())