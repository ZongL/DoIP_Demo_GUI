#import os
import sys
from doipclient import DoIPClient
import binascii

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import QTimer
from Diagnostic_DownLoad import *
import subprocess

# coding=utf8


def enterDefaultSession(doip_client):
        #进默认会话
        print('session control send ', doip_client.send_diagnostic(b'\x10\x01'))
        print('session control recv ', doip_client.receive_diagnostic())

def enterExtendSession(doip_client):
        #进拓展会话
        doip_client.send_diagnostic(b'\x10\x03')
        print('extend session control send ',(b'\x10\x03'))
        print('extend session control recv ', doip_client.receive_diagnostic())

def unlock_SecurityAccess(doip_client):
    doip_client.send_diagnostic(b'\x27\x01')
    print('unlock_SecurityAccess send ',(b'\x27\x01'))
    seed = doip_client.receive_diagnostic()
    print('unlock_SecurityAccess recv ', seed)
    seed = seed[2:]
    key = SeedToKey(int.from_bytes(seed,'big'),mask)
    request = bytearray(b'\x27\x02')
    request.extend(key.to_bytes(4,'big'))
    #doip_client.send_diagnostic(b'\x27\x12\xc4\x4e\xeb\xe8')
    doip_client.send_diagnostic(request)
    print('unlock_SecurityAccess send ',request)
    AccessResult=doip_client.receive_diagnostic()
    print('unlock_SecurityAccess recv ', AccessResult)
    return AccessResult

def TesterPresent(doip_client):
    doip_client.send_diagnostic(b'\x3E\x00')
    print('TesterPresent recv ', doip_client.receive_diagnostic())

def readMcuVIN(doip_client_mcu):
    data = bytearray(b'\x22\xCF\x4A') # 立时读did
    doip_client_mcu.send_diagnostic(data)
    response = doip_client_mcu.receive_diagnostic()


def readDTC(doip_client_mcu):
    data = (binascii.a2b_hex('190676001DFF'))
    #data = (binascii.a2b_hex('1902FF'))

    doip_client_mcu.send_diagnostic(data)
    print('读取 ' + 'DTC ' + ': ', str(binascii.hexlify((data))))
    response = doip_client_mcu.receive_diagnostic()
    print('获得 ' + 'DTC ' + ': ', str(binascii.hexlify(response)))  # str(binascii.hexlify((response)))



class MyWindow(QMainWindow, Ui_MainWindow):
#class MyWindow(QWidget, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent=parent)
        self.setupUi(self)

        self.selectECUname='0040'

        #chatgpt 2023-7-31
        # Create a QTimer instance
        self.timer = QTimer(self)
        # Set the interval in milliseconds (4 seconds in this case)
        self.timer.setInterval(4000)  # 4000 milliseconds = 4 seconds
        # Connect the timeout signal to the TesterPresent function
        self.timer.timeout.connect(self.TesterPresent)
        #event
        self.pushButton_2.clicked.connect(self.checkconnectornot)  #连接
        self.pushButton_3.clicked.connect(self.closeit) #duankai
        #self.comboBox_3.currentIndexChanged.connect(self.selectecu_)  #输入
        self.pushButton_13.clicked.connect(self.sendreq_)             #发送
        #self.graphicsView.setBackgroundBrush(qcc.green(self))
        self.radioButton_3.clicked.connect(self.Extendedsection)  #Extended section
        self.radioButton.clicked.connect(self.defaultsection)   #default section
        self.checkBox.stateChanged.connect(self.toggle_timer)
        self.textEdit.moveCursor(self.textEdit.textCursor().End)

        self.FuncOkorNOK_NOK()
    def FuncOkorNOK_NOK(self):
        self.checkBox.setEnabled(False)
        self.pushButton_13.setEnabled(False)
        self.pushButton_2.setStyleSheet('''QPushButton{background:#FFFFC0;}''')
        self.radioButton_3.setEnabled(False)
        self.radioButton.setEnabled(False)
        self.radioButton_2.setEnabled(False)
    def FuncOkorNOK_OK(self):
        self.pushButton_13.setEnabled(True)
        self.pushButton_2.setStyleSheet('''QPushButton{background:#40FF80;}''')
        self.checkBox.setEnabled(True)
        self.radioButton_3.setEnabled(True)
        self.radioButton.setEnabled(True)
    def checkconnectornot(self):
        if is_host_reachable(target_ecu_ip):
            self.createconnect()
        else:
            self.textEdit.append("please connect Tx to ECU or ECU no response")

    def createconnect(self):
        self.doip_client_mcu = DoIPClient(target_ecu_ip, target_ecu_logical_address, protocol_version=0x03, client_logical_address=source_client_logical_address)
        self.FuncOkorNOK_OK()

    def closeit(self):
        self.doip_client_mcu.close()
        self.FuncOkorNOK_NOK()

    def selectecu_(self):
        if self.comboBox_3.currentText() == 'VDP':
            self.selectECUname='0040'
        else:
            self.selectECUname = '1FFF'
        self.lineEdit_2.setText(self.selectECUname)
    def sendreq_(self):
        inputcmd = self.lineEdit.text()
        if inputcmd != '':
            reqdata = (binascii.a2b_hex(inputcmd))
            self.doip_client_mcu.send_diagnostic(reqdata)
            print('读取 ' + 'DTC ' + 'VDP MCU 物流数据: ', str(binascii.hexlify(reqdata)))
            self.textEdit.append(binascii.hexlify(reqdata).decode().upper())
            response = self.doip_client_mcu.receive_diagnostic()
            print('获得 ' + 'DTC ' + 'VDP MCU 物流数据: ',str(binascii.hexlify(response)))
            self.textEdit.append(binascii.hexlify(response).decode().upper())
            self.textEdit.append(str(response))
    def Extendedsection(self):
        self.textEdit.append("1003")
        enterExtendSession(self.doip_client_mcu)
        AccessresulttoTXT=unlock_SecurityAccess(self.doip_client_mcu)
        self.textEdit.append(binascii.hexlify(AccessresulttoTXT).decode().upper())


    def toggle_timer(self, state):
        if state == 2:  # Qt.Checked
        # Start the timer when the checkBox is checked
            self.timer.start()
        else:
        # Stop the timer when the checkBox is unchecked
            self.timer.stop()
    def TesterPresent(self):
        TesterPresent(self.doip_client_mcu)
        self.textEdit.append("3E00")
    def defaultsection(self):
        self.textEdit.append("1001")
        enterDefaultSession(self.doip_client_mcu)

def is_host_reachable(ip_address):
    # 在Windows上使用"ping"命令
    if subprocess.call(["ping", "-n", "1", ip_address]) == 0:
        return True
    else:
        return False



if __name__ =='__main__':
    # 目标IP地址
    target_ecu_ip = 'xxxxxxxx.xxxx.xxxx.xxxx'
    # 目标逻辑地址
    target_ecu_logical_address = 0x40 #
    source_client_logical_address = 0xF00 # 0x0E80
    is_host_reachable(target_ecu_ip)
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())

