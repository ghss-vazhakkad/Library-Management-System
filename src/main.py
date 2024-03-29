import sys
from PyQt5 import uic
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtWidgets import *
from login import Login
from bookentry import *
from refbook import *
from openpyxl import Workbook, load_workbook
from PyQt5.QtGui import QPixmap
from member import *
class Dialog(QDialog):
    def __init__(self,title,message):
        super(Dialog,self).__init__()
        uic.loadUi('res/dialog.ui',self)
        self.setWindowTitle(title)
        self.setFixedSize(self.size())
        self.message.setText(message)
        
        self.show()

logindata = [""]
book = Book()
class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi('res/main.ui', self)
        self.ciec.setVisible(False)
        self.actionBookShowList.triggered.connect(self.circulate)
        self.loginBtn.clicked.connect(self.login)
        self.actionAddMember.triggered.connect(self.addmember)
        self.userdata = logindata
        self.loadbooks()
        self.adminuser = False
        self.setFixedSize(self.size())
        self.bookclk = self.memberclk = False
        self.loadmembers()
        
        self.actionIssueBook.triggered.connect(self.issue)
        self.actionAddBook.triggered.connect(self.addbook)
        self.actionReserveBook.triggered.connect(self.reserve)
        self.actionReportBooks.triggered.connect(self.bookReport)
        self.actionReportMembers.triggered.connect(self.reportMember)
        self.memberList.clicked.connect(self.onSelectMember)
        self.bookList.clicked.connect(self.onSelectBook)
        self.actionEditBook.triggered.connect(self.edit)
        self.actionDeleteBook.triggered.connect(self.deleteBook)
        self.actionDeleteMember.triggered.connect(self.deleteMember)
        self.actionEditMember.triggered.connect(self.editMember)
        self.memberSearch.textChanged.connect(self.onSearchMember)
        self.bookSearch.textChanged.connect(self.onSearchBook)
        #self.access = "ADMIN"
        self.isListShown = False
        #self.logged()
        self.showMaximized()
    def bookReport(self):
        self.qwinreport = BookReport(self)
    def reportMember(self):
        self.qwinreport = ReportMember(self)
    def circulate(self):
        if(not self.isListShown):
            self.ciec.setVisible(True)
            self.lig.setVisible(False)
            self.actionBookShowList.setText("Hide list")
        else:
            self.ciec.setVisible(False)
            self.lig.setVisible(True)
            self.actionBookShowList.setText("Show list")
        self.isListShown = not self.isListShown
    def getLastBookID(self):
        id=0
        for book in self.books:
            if(book.id > id):
                id = book.id
        
        id+=1
        return id
    def getLastMemberID(self):
        id=0
        for member in self.members:
            if(member.id > id):
                id = member.id
        return id+1
    def deleteMember(self):
        b = self.memberList.currentIndex().row()
        book = self.member[b]
        book.delete("data/members.xlsx")
        self.qwindialdel = Dialog("Member removed",book.name+" is removed")
        self.actionDeleteMember.setEnabled(False)
        self.loadmembers()
    def editMember(self):
        member = self.member[self.memberList.currentIndex().row()]
        self.qwinedit = EditMember(self,member)
    def deleteBook(self):
        b = self.bookList.currentIndex().row()
        book = self.book[b]
        book.delete(Book.DATA_FILE)
        self.qwindialdel = Dialog("Book removed",book.title+" is removed")
        self.actionDeleteBook.setEnabled(False)
        self.loadbooks()
    def edit(self):
        b = self.bookList.currentIndex().row()
        book = self.book[b]
        self.qwinedit = BookEdit(self,book)
    def onSearchMember(self):
        text = str(self.memberSearch.text())
        self.actionDeleteMember.setEnabled(False)
        self.actionIssueBook.setEnabled(False)
        self.membersearchmodel = QStandardItemModel()
        if(text == ""):
            self.memberList.setModel(self.membermodel)
            self.member = self.members.copy()
        else:
            self.memberList.setModel(self.membersearchmodel)
            self.member = []
            for member in self.members:
                if(text.upper() in member.name.upper() or text in str(member.id)):
                    self.member.append(member)
                    item = QStandardItem(str(member.id).zfill(4)+" | "+member.name)
                    item.setEditable(False)
                    self.membersearchmodel.appendRow(item)
        

    def onSearchBook(self):
        text = str(self.bookSearch.text())
        self.booksearchmodel = QStandardItemModel()
        self.actionIssueBook.setEnabled(False)
        self.actionEditBook.setEnabled(False)
        self.actionDeleteBook.setEnabled(False)
        if(text == ""):
            self.bookList.setModel(self.bookmodel)
            self.book = self.books.copy()
        else:
            self.bookList.setModel(self.booksearchmodel)
            self.book = []
            if(text.startswith(":")):
                prefix = text.split(":")[1]
                print(prefix.upper())
                if prefix.upper() == "ISSUED":
                   for book in self.books:
                       if(book.issued != "none"):
                           self.book.append(book)
                           item = QStandardItem(book.title)
                           item.setEditable(False)
                           self.booksearchmodel.appendRow(item)
                elif prefix.upper() == "RESERVED":
                   for book in self.books:
                       if(book.issued == "none"):
                           self.book.append(book)
                           item = QStandardItem(book.title)
                           item.setEditable(False)
                           self.booksearchmodel.appendRow(item) 
                return
                    

            for book in self.books:
                if(book.title.upper().startswith(text.upper())):
                    self.book.append(book)
                    item = QStandardItem(book.title)
                    item.setEditable(False)
                    self.booksearchmodel.appendRow(item)

    def onSelectBook(self,index):
        book = self.book[index.row()]
        self.bookclk = True
        if(self.adminuser):
            self.actionReserveBook.setEnabled(book.issued != "none")
            self.actionEditBook.setEnabled(True) 
            self.actionDeleteBook.setEnabled(True)
        if(self.memberclk and self.bookclk and self.adminuser):
            self.actionIssueBook.setEnabled(True)      
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
            book.writetosheet(Book.DATA_FILE)
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

            book.writetosheet(Book.DATA_FILE)
            self.issued = Dialog("Book Issued",book.title+" issued to "+member.name)
            self.actionReserveBook.setEnabled(True)
        else:
            self.issued = Dialog("Book Already Issued","Book already issued to "+Member.fgetMemberById(eval(book.issued),self.members).name)

        pass
    def onSelectMember(self):
        self.memberclk = True

        if(self.adminuser):
            self.actionDeleteMember.setEnabled(True)
            self.actionEditMember.setEnabled(True) 
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
            item = QStandardItem(str(member.id).zfill(4)+" | "+member.name)
            item.setEditable(False)
            self.membermodel.appendRow(item)
    def loadbooks(self):
        self.bookmodel = QStandardItemModel()
        self.bookList.setModel(self.bookmodel)
        bookxl = load_workbook(Book.DATA_FILE)
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
        self.bookmenu = [self.actionAddMember,self.actionAddBook,self.actionBookShowList,self.actionReportMembers,self.actionReportBooks]
        self.adminuser = True
        self.loginBtn.setVisible(False)
        if(state):
            for action in self.bookmenu:
                action.setEnabled(True)

stylesheet = """
Main{
    background-image:url("res/splash.png");
    background-color:#000000;
    background-position:center;
}
"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    window = Main()
    sys.exit(app.exec_())