from PyQt6.QtWidgets import QWidget, QPushButton, QLineEdit
from PyQt6 import uic
from DBchet import DBchet


class log(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./login.ui', self)
        self.logindb = self.findChild(QPushButton, 'logindb')
        self.name = self.findChild(QLineEdit, 'name')
        self.password = self.findChild(QLineEdit, 'password')
        self.logindb.clicked.connect(self.jump)

    #登陆按钮槽函数
    def jump(self):
        na = self.name.text() #获取当前lineEdit输入的文本
        pa = self.password.text()
        # 数据库查询校验操作

        self.DB = DBchet(n=na)
        self.DB.show()
        self.close()
