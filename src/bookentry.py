import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *


class BookEntry(QDialog):
    def __init__(self):
        super(BookEntry, self).__init__()
        uic.loadUi('res/bookentry.ui', self)
        self.show()
class BookItem(QWidget):
    def __init__(self):
        super(BookItem, self).__init__()
        uic.loadUi('res/widgets/bookitem.ui', self)
class Book:
    BOOKTYPE_GENERAL = 10
    BOOKTYPE_REFERENCE = 11
    TYPE_DIRECT = 0
    TYPE_DONATION = 1
    TYPE_GIFT = 2

    def __init__(self):
        self.date = [0,0,0]
        self.title = ""
        self.id = 0
        self.subject = ""
        self.language = ""
        self.price = 0
        self.publisher = ""
        self.year = 0
        self.booktype = 0
        self.copies = 0
        self.type = 0
    def loadfromrow(row):
        rt = Book()
        dt=str(row[0].value).split("-")
        rt.date[0]=eval(dt[0])
        rt.date[1]=eval(dt[1])
        rt.date[2]=eval(dt[2])
        rt.title =str(row[1].value)
        rt.id = eval(str(row[2].value))
        rt.subject = str(row[3].value)
        rt.language = str(row[4].value)
        rt.price = eval(str(row[5].value))
        rt.publisher = str(row[6].value)
        rt.year = eval(str(row[7].value))
        rt.booktype = eval(str(row[8].value))
        rt.type = eval(str(row[9].value))
 
        return rt
