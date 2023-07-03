import sys
from PyQt5 import uic;
from PyQt5.QtWidgets import *;
from openpyxl import Workbook, load_workbook

userdata = []

class Login(QWidget):

    def __init__(self,parent):
        super(Login, self).__init__()
        uic.loadUi('res/login.ui', self)
        self.setFixedSize(self.size())
        self.username.setText(parent.userdata[0])
        self.parent = parent
        self.loginButton.clicked.connect(self.trylogin)
        self.show()
    def trylogin(self,iscl):
        uname = str(self.username.text())
        upass = str(self.password.text())
        users = load_workbook("data/users.xlsx")
        userd = users["Main"]["A"]
        passd = users["Main"]["B"]
        accessd = users["Main"]["C"]
        i=1
        while i < len(userd):
            user = str(userd[i].value)
            passw = str(passd[i].value)
            if(user == uname and passw == upass):
                # login worked
                print("Logged in as ",user)
                self.parent.access = str(accessd[i].value)
                self.parent.logged()
                self.hide()
            i+=1


                    
