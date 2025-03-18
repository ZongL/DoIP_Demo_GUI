#import os
import sys
from doipclient import DoIPClient
import binascii

#from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from Diagnostic_DownLoad import *
# coding=utf8

class MyWindow(QMainWindow, Ui_MainWindow):
#class MyWindow(QWidget, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent=parent)
        self.setupUi(self)

        self.selectECUname='0040'

        #event
        #self.pushButton_2.clicked.connect(self.ConnectToDoIPServer_)  #连接
        #self.pushButton_3.clicked.connect(self.DisconnectFromDoIPServer_) #duankai
        #self.comboBox_3.currentIndexChanged.connect(self.selectecu_)  #输入
        self.pushButton_13.clicked.connect(self.sendreq_)             #发送
        #self.graphicsView.setBackgroundBrush(QColor.green())
        #self.radioButton_3.clicked.connect(self.DoIPSwitchDiagnosticSession_)
        #self.radioButton_2.clicked.connect(self.DoIPSA_)
        #self.checkBox.stateChanged.connect(self.choose)
        self.textEdit.moveCursor(self.textEdit.textCursor().End)
        #self.CheckConnection()

    def selectecu_(self):
        if self.comboBox_3.currentText() == 'ecu':
            self.selectECUname='0040'
        else:
            self.selectECUname = '1FFF'
        self.lineEdit_2.setText(self.selectECUname)
    def sendreq_(self):
        inputcmd = self.lineEdit.text()
        if inputcmd != '':
            data = (binascii.a2b_hex(inputcmd))
            doip_client_mcu.send_diagnostic(data)
            self.textEdit.append(binascii.hexlify(data).decode().upper())
            response = doip_client_mcu.receive_diagnostic()
            self.textEdit.append((binascii.hexlify(response).decode().upper()))

if __name__ =='__main__':
    target_ecu_ip = 'xxx.xx.xx.xx'
    target_ecu_logical_address = 0x40
    source_client_logical_address = 0xF00
    doip_client_mcu = DoIPClient(target_ecu_ip, target_ecu_logical_address, protocol_version=0x03, client_logical_address=source_client_logical_address)
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
