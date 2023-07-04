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
    def __init__(self,title,message):
        super(Dialog,self).__init__()
        uic.loadUi('res/dialog.ui',self)
        self.setWindowTitle(title)
        self.setFixedSize(self.size())
        self.message.setText(message)
        
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

        self.adminuser = False
        self.bookclk = self.memberclk = False
        self.loadmembers()
        self.actionIssueBook.triggered.connect(self.issue)
        self.actionAddBook.triggered.connect(self.addbook)
        self.actionReserveBook.triggered.connect(self.reserve)
        self.memberList.clicked.connect(self.onSelectMember)
        self.bookList.clicked.connect(self.onSelectBook)
        self.memberSearch.textChanged.connect(self.onSearchMember)
        self.bookSearch.textChanged.connect(self.onSearchBook)
        # self.access = "ADMIN"
        # self.logged()
        self.show()
    def onSearchMember(self):
        text = str(self.memberSearch.text())
        self.actionIssueBook.setEnabled(False)
        self.membersearchmodel = QStandardItemModel()
        if(text == ""):
            self.memberList.setModel(self.membermodel)
            self.member = self.members.copy()
        else:
            self.memberList.setModel(self.membersearchmodel)
            self.member = []
            for member in self.members:
                if(member.name.startswith(text)):
                    self.member.append(member)
                    item = QStandardItem(member.name)
                    item.setEditable(False)
                    self.membersearchmodel.appendRow(item)
        

    def onSearchBook(self):
        text = str(self.bookSearch.text())
        self.booksearchmodel = QStandardItemModel()
        self.actionIssueBook.setEnabled(False)
        if(text == ""):
            self.bookList.setModel(self.bookmodel)
            self.book = self.books.copy()
        else:
            self.bookList.setModel(self.booksearchmodel)
            self.book = []
            for book in self.books:
                if(book.title.startswith(text)):
                    self.book.append(book)
                    item = QStandardItem(book.title)
                    item.setEditable(False)
                    self.booksearchmodel.appendRow(item)

    def onSelectBook(self,index):
        book = self.book[index.row()]
        self.bookclk = True
        self.actionReserveBook.setEnabled(book.issued != "none")    
        pass
    def addmember(self):
        self.addmem = AddMember(self)
    def login(self,b):
        self.window1 = Login(self)
    def logged(self):
        if(self.access == "ADMIN"):
            self.admin(True)
    def reserve(self):
        b = self.bookList.currentIndex().row()
        book = self.book[b]
        if(book.issued != "none"):
            oldmem = Member.fgetMemberById(eval(book.issued),self.members).name
            book.issued = "none"
            book.replace("data/books.xlsx")
            self.actionReserveBook.setEnabled(False)  
            self.rd1 = Dialog("Book reserved",book.title+" has been reserved from "+oldmem)
        else:
            self.rd1 = Dialog("Already reserved",book.title+" already reserved")

    def issue(self):
        b = self.bookList.currentIndex().row()
        m = self.memberList.currentIndex().row()
        book = self.book[b]
        member = self.member[m]
        if(book.issued == "none"):
            book.issued = str(member.id)
            book.replace("data/books.xlsx")
            self.issued = Dialog("Book Issued",book.title+" issued to "+member.name)
            self.actionReserveBook.setEnabled(True)
        else:
            self.issued = Dialog("Book Already Issued","Book already issued to "+Member.fgetMemberById(eval(book.issued),self.members).name)

        pass
    def onSelectMember(self):
        self.memberclk = True
        if(self.memberclk and self.bookclk and self.adminuser):
            self.actionIssueBook.setEnabled(True)
    def addbook(self):
        self.addwin = BookEntry(self)
    def loadmembers(self):
        self.membermodel = QStandardItemModel()
        self.memberList.setModel(self.membermodel)
        self.members = Member.load("data/members.xlsx")
        self.member = self.members.copy()
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
        self.book = self.books.copy()
    
    def admin(self,state):
        self.bookmenu = [self.actionAddMember,self.actionAddBook]
        self.adminuser = True
        if(state):
            for action in self.bookmenu:
                action.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())