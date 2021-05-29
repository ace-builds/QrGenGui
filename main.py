from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QFileDialog,QApplication, QPushButton, QLineEdit, QComboBox, QTimeEdit, QDateEdit,QMessageBox
from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5 import QtGui
import PyQt5
import sys, requests as rq
from PyQt5.QtCore import pyqtSignal,pyqtSlot

req_str = f"http://chart.apis.google.com/chart?cht=qr&chs=500x500&chl=https%3Auplitemedia.com&chld=H|0"
class QrGen(QtWidgets.QMainWindow):
    def __init__(self):
        super(QrGen, self).__init__()
        uic.loadUi("qrgen.ui", self)
        self.generate.clicked.connect(self.generateQr)
        self.clear.clicked.connect(self.clearTxtbox)
        self.sideThread = requestThread()
        
        self.show()

    def generateQr(self):
        if not self.url.toPlainText():
            self.messageB("Insert URL")
        elif self.generate.text().lower() == 'save':
            self.saveFunc()
        else:
            try:
                req_str = f"http://chart.apis.google.com/chart?cht=qr&chs=500x500&chl={self.url.toPlainText()}&chld=H|0"
                self.sideThread.run(req_str)
                while self.sideThread.done != True:
                    pass
                
                self.setFinal()
            except rq.RequestException:
                self.messageB("Could not connect to internet, check your internet connection and try again")
                
            except Exception:
               self.messageB("Contact Developer")
    def saveFunc(self):
        name = QFileDialog.getSaveFileName(self, 'Save File',"Qrcode.png", "Image files (*.png)")
    def messageB(self,str):
        msg1= QMessageBox()
        msg1.setText(str)
        msg1.setWindowTitle("QR code generator")
        msg1.exec_()

    def clearTxtbox(self):
        self.url.setText("")
        self.img.setPixmap(QtGui.QPixmap("meme.png"))
        self.generate.setText("Generate QR code")
    
    def setFinal(self):
        self.img.setPixmap(QtGui.QPixmap("images/img.png"))
        self.generate.setText("Save")

class requestThread(QtCore.QThread):
    def __init__(self, parent=None):
        super(requestThread, self).__init__(parent)
        self.done =False
    
    def run(self,link):
        response = rq.get(link)
        file = open(f"images/img.png", "wb")
        file.write(response.content)
        file.close()
        self.done = True
    def close(self):
        self.terminate()

app = QApplication(sys.argv)
UIWindow = QrGen()
app.exec_()
