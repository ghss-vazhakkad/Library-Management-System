import sys
from PyQt5 import uic
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtWidgets import *
from login import Login
from bookentry import *
from refbook import RefBook
from openpyxl import Workbook, load_workbook


logindata = ["Ihjas"]
book = Book()
class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi('res/main.ui', self)
        self.actionModifyBook.triggered.connect(self.login)
        self.userdata = logindata
        self.loadbooks()
        self.actionAddBook.triggered.connect(self.addbook)
        self.show()
    def login(self,b):
        self.window1 = Login(self)
    def logged(self):
        if(self.access == "ADMIN"):
            self.admin(True)
    def addbook(self):
        self.addwin = BookEntry(self)
    def loadbooks(self):
        self.bookmodel = QStandardItemModel()
        self.bookList.setModel(self.bookmodel)
        bookxl = load_workbook("data/books.xlsx")
        main = len(bookxl["Main"]["A"])
        self.books = []
        for i in range(1,main):
            sample = str(bookxl["Main"][i+1][0].value)
            if(sample != "None"): self.books.append(Book.loadfromrow(bookxl["Main"][i+1]))
        for book in self.books:
            item = QStandardItem(book.title)
            item.setEditable(False)
            self.bookmodel.appendRow(item)
    def admin(self,state):
        self.bookmenu = [self.actionAddBook,self.actionEditBook,self.actionDeleteBook,self.actionIssueBook,self.actionReserveBook,self.actionSearchBook]
        if(state):
            for action in self.bookmenu:
                action.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())