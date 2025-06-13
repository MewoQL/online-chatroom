from PyQt6.QtWidgets import QWidget, QPushButton, QLineEdit, QTextEdit, QMessageBox
from PyQt6 import uic
import socket
from PyQt6.QtCore import QThread, pyqtSignal
import time


class re_thread(QThread):
    update = pyqtSignal(str)

    def __init__(self, tcpc):
        super().__init__()
        self.tcp = tcpc

    def run(self):
        while True:
            try:
                data = self.tcp.recv(1024)
                if data:
                    self.update.emit(data.decode("utf-8"))
                else:
                    break
            except Exception as e:
                print(f"数据接受错误{e}")
                break


class DBchet(QWidget):
    def __init__(self, n):
        super().__init__()
        uic.loadUi('DBchet.ui', self)
        self.name = n
        self.chet = self.findChild(QTextEdit, 'chet')
        self.sent = self.findChild(QPushButton, 'sent')
        self.write = self.findChild(QTextEdit, 'write')
        self.tcp = None
        self.th = None
        self.connect_server()
        self.sent.clicked.connect(self.sendm)

    def connect_server(self):
        server_ip = ""
        server_port = 2025
        try:
            self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp.connect((server_ip, server_port))
            self.tcp.sent(self.name.encode('utf-8'))
            print("现在发完名字了")
        except Exception as e:
            print(f"名字或者客户端链接服务器出错{e}")

        self.th = re_thread(self.tcp)
        self.th.update.connect(self.update_ui)
        self.th.start()

    def update_ui(self, data):
        self.chet.append(data)

    def sendm(self):
        if not self.tcp:
            print("没链接上服务器，发啥呢")
            return
        try:
            massage = self.write.toPlainText()
            if massage:
                self.tcp.send(massage.encode('utf-8'))
                time.sleep(0.05)
            else:
                QMessageBox.warning(self, "警告", "发送消息为空")
        except ConnectionAbortedError:
            print("链接被终止")
            return -1
        except ConnectionResetError:
            print("连接重置断开")
            return -1
        except Exception as e:
            print(f"异常：{e}")
            return -1

    def closeEvent(self, event):
        if self.th:
            self.th.stop()
            self.th.wait()
        if self.tcp:
            self.tcp.close()
        event.accept()
        
