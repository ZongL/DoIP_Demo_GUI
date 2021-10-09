# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from Diagnostic_DownLoad import *
from PyDoIP import *

#pyuic5 -o Diagnostic_DownLoad.py Diagnostic_DownLoad.ui

class MyWindow(QMainWindow, Ui_MainWindow):
#class MyWindow(QWidget, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent=parent)
        self.setupUi(self)



        #event
        self.pushButton_2.clicked.connect(self.ConnectToDoIPServer_)  #连接
        self.pushButton_3.clicked.connect(self.DisconnectFromDoIPServer_) #duankai
        self.comboBox_3.currentIndexChanged.connect(self.selectecu_)  #输入
        self.pushButton_13.clicked.connect(self.sendreq_)             #发送
        #self.lineEdit.textEdited[str].connect(lambda:self.lineEditonChange())


    def selectecu_(self):
        self.lineEdit_2.setText(self.comboBox_3.currentText())
    def sendreq_(self):
        inputcmd = self.lineEdit.text()
        imputfilter=inputcmd.replace(' ','')
        #DoIPClient.DoIPReadDID(PyUDS.DID_VINIDNO)
        if imputfilter[0:2] == '22':
            DoIPClient.DoIPReadDID(imputfilter[2:6])
            #DoIPClient.DoIPReadDID('F190')
            #print(imputfilter)
    #def lineEditonChange(self):
    #    facename = self.lineEdit.text()
    #    print(facename)
    #    print(type(facename))


    def ConnectToDoIPServer_(self):
        DoIPClient.ConnectToDoIPServer(routingActivation=True)
    def DisconnectFromDoIPServer_(self):
        DoIPClient.DisconnectFromDoIPServer()
    def RequestRoutingActivation_(self):
        DoIPClient.RequestRoutingActivation(localECUAddr='0E02', targetECUAddr='0C02')
    def DoIPReadDID_(self):
        DoIPClient.DoIPReadDID(PyUDS.DID_VINIDNO)

if __name__ == '__main__':
    #new class
    DoIPClient = DoIP_Client()
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
