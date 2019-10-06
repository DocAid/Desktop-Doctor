from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import requests
from opening import Ui_DocAid
from homepage import Ui_MainWindow
from prescription import Ui_Prescription
from report import Ui_Report

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
        self.homepage.setupUi(self)
        self.homepage.pushButton.clicked.connect(self.goPrescription)
        self.show()
    
    def goPrescription(self):
        self.report.setupUi(self)
        # self.homepage.pushButton.setText("Clicked")
        # self.prescription.setupUi(self)
        self.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())