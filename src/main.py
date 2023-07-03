import sys
from PyQt5 import uic
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtWidgets import *
from login import Login
from bookentry import *
from refbook import RefBook
from openpyxl import Workbook, load_workbook
from member import *
class Dialog(QDialog):
    def __init__(self):
        super(Dialog,self).__init__()
        uic.loadUi('res/dialog.ui',self)
        self.setFixedSize(self.size())
        self.show()

logindata = ["Ihjas"]
book = Book()
class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi('res/main.ui', self)
        self.setFixedSize(self.size())
        self.actionModifyBook.triggered.connect(self.login)
        self.actionAddMember.triggered.connect(self.addmember)
        self.userdata = logindata
        self.loadbooks()
        self.clk = -1
        self.loadmembers()
        self.actionIssueBook.triggered.connect(self.issue)
        self.actionAddBook.triggered.connect(self.addbook)
        self.memberList.clicked.connect(self.selectmem)
        self.bookList.clicked.connect(self.selectmem)
        self.show()
    def addmember(self):
        self.addmem = AddMember(self)
    def login(self,b):
        self.window1 = Login(self)
    def logged(self):
        if(self.access == "ADMIN"):
            self.admin(True)
    def issue(self):
        b = self.bookList.currentIndex().row()
        m = self.memberList.currentIndex().row()
        book = self.books[b]
        member = self.members[m]
        book.issued = str(member.id)
        book.replace("data/books.xlsx")
        self.issued = Dialog()
        pass
    def selectmem(self,i):
        self.clk+=1
        if(self.clk >= 1):
            self.actionIssueBook.setEnabled(True)
    def addbook(self):
        self.addwin = BookEntry(self)
    def loadmembers(self):
        self.membermodel = QStandardItemModel()
        self.memberList.setModel(self.membermodel)
        self.members = Member.load("data/members.xlsx")
        for member in self.members:
            item = QStandardItem(member.name)
            item.setEditable(False)
            self.membermodel.appendRow(item)
    def loadbooks(self):
        self.bookmodel = QStandardItemModel()
        self.bookList.setModel(self.bookmodel)
        bookxl = load_workbook("data/books.xlsx")
        main = len(bookxl["Main"]["A"])
        self.books = []
        for i in range(1,main):
            sample = str(bookxl["Main"][i+1][0].value)
            if(sample != "None" and sample != ""): 
                book = Book.loadfromrow(bookxl["Main"][i+1])
                book.row = i+1
                self.books.append(book)
        for book in self.books:
            item = QStandardItem(book.title)
            item.setEditable(False)
            self.bookmodel.appendRow(item)
    
    def admin(self,state):
        self.bookmenu = [self.actionAddMember,self.actionAddBook,self.actionEditBook,self.actionDeleteBook]
        if(state):
            for action in self.bookmenu:
                action.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())