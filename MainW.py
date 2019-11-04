import sys
import socket
from UI import *
from PyQt5.QtWidgets import *

class DemoUI(QMainWindow, Ui_MainWindow):

    def __init__(self,parent = None):
        super(DemoUI,self).__init__(parent)
        self.setupUi(self)
        self.setupParam()
    def setupParam(self):
        self.text = b''
        self.ip = ''
        self.port = 0
        self.showSent = 0
        self.showRecv = 0
        self.TPS = 0
        self.Num = 0
        self.tempNum = 0
        self.recvLog = ''
        self.textFormat = 'UTF-8'
        self.C = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lineEdit.textChanged[str].connect(self.textChanged)
        self.lineEdit_2.textChanged[str].connect(self.ipChanged)
        self.lineEdit_3.textChanged[str].connect(self.portChanged)
        self.lineEdit_4.textChanged[str].connect(self.formatChanged)
        self.lineEdit_7.textChanged[str].connect(self.tpsChanged)
        self.lineEdit_8.textChanged[str].connect(self.numChanged)
        self.sendButton.clicked.connect(self.send)
        self.sendButton_2.clicked.connect(self.stop)
        self.checkBox_2.clicked.connect(self.showSentText)
        self.checkBox_3.clicked.connect(self.showRecvText)

    def textChanged(self,text):
        self.text = text.encode(self.textFormat)
        print('text: ', self.text)
    def ipChanged(self,ip):
        self.ip = ip
        print('ip: ', self.ip)
    def portChanged(self,port):
        self.port = port
        print('port: ', self.port)
    def formatChanged(self,format):
        self.format = format
        print('format: ', self.format)
    def tpsChanged(self,tps):
        self.tps = tps
        print('tps: ', self.tps)
    def numChanged(self,num):
        self.num = num
        print('num: ', self.num)
    def showSentText(self):
        if self.checkBox_2.checkState():
            self.showSent = 1
        else:
            self.showSent = 0
        print('showSent:' , self.showSent)
    def showRecvText(self):
        if self.checkBox_3.checkState():
            self.showRecv = 1
        else:
            self.showRecv = 0
        print('showRecv:' ,self.showRecv)
    def send(self):
        res = self.parmCheck()
        if res:
            QMessageBox.information(self, "参数错误", res)
        #首次发送
        if not self.tempNum:
            try:
                self.C.connect((self.ip, self.port))
            except:
                self.plainTextEdit_2.appendPlainText('连接失败，请检查ip端口填写以及服务器开启情况。')
                QMessageBox.information(self, "连接失败", "请检查ip端口填写以及服务器开启情况。")
                return 'Error occurs while trying connecting ...'
            self.plainTextEdit_2.appendPlainText('首次Socket连接成功。')
            self.C.send(self.text)
            if self.showSent:self.plainTextEdit_2.appendPlainText(self.text)
            data = self.C.recv(1024)
            if self.showRecv: self.plainTextEdit_2.appendPlainText(data)
            self.tempNum += 1
        #循环发送
        else:
            while(self.tempNum < self.num):
                try:
                    self.C.send(self.text)
                except:
                    self.plainTextEdit_2.appendPlainText('socket已断开，重连中...')
                    try:
                        self.C.connect((self.ip, self.port))
                        self.plainTextEdit_2.appendPlainText('socket已重连，继续发送')
                    except:
                        self.plainTextEdit_2.appendPlainText('重连失败，已退出，请检查网络。')
                if self.showSent: self.plainTextEdit_2.appendPlainText(self.text)
                data = self.C.recv(1024)
                if self.showRecv: self.plainTextEdit_2.appendPlainText(data)
                self.tempNum += 1
            self.plainTextEdit_2.appendPlainText('发送完毕，共发送', self.tempNum, '笔')
    def stop(self):
        pass
    def parmCheck(self):
        if not self.text: return '未输入发送报文'
        if not self.ip: return '未输入发送IP'
        if not self.port: return '未输入发送端口'
        if not self.tps: return '未输入TPS'
        return 0
if __name__ == '__main__':    #Test Part
    app = QApplication(sys.argv)
    w = DemoUI()
    w.show()
    sys.exit(app.exec_())
