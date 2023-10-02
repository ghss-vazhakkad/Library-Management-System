import sys
import typing
from PyQt5 import QtCore, uic;
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from member import Member
from PyQt5.QtGui import QStandardItemModel,QStandardItem

class BookReport(QDialog):
    def __init__(self, parent):
        super(BookReport,self).__init__()
        uic.loadUi("res/bookreport.ui",self)
        self.loadbooks(parent)
        self.setFixedSize(self.size())
        self.show()
    def loadbooks(self,parent):
        self.model = QStandardItemModel()
        self.tableView.setModel(self.model)
        self.titles = ["ID","Title","Subject","Language","Issued to"]
        tcol = []
        for t in self.titles:
            item = QStandardItem(t)
            item.setEditable(False)
            tcol.append(item)
        self.model.appendRow(tcol)
        for book in parent.books:
            self.titles = [str(book.id),book.title,book.subject,book.language,"Reserved"]
            icol = []
            if(str(book.issued) != "none"):
                try:
                    self.titles[4] = Member.fgetMemberById(eval(book.issued),parent.members).name
                except:
                    book.issued = "none"

            for t in self.titles:
                item = QStandardItem(t)
                item.setEditable(False)
                icol.append(item)
            self.model.appendRow(icol)
        pass

class ReportMember(QDialog):
    def __init__(self,parent):
        super(ReportMember,self).__init__()
        uic.loadUi("res/reportmember.ui",self)
        self.setFixedSize(self.size())
        self.loadmembers(parent)
        self.show()
    def loadmembers(self,parent):
        self.model = QStandardItemModel()
        self.tableView.setModel(self.model)
        self.titles = ["ID","Name","Status"]
        tcol = []
        for t in self.titles:
            item = QStandardItem(t)
            item.setEditable(False)
            tcol.append(item)
        self.model.appendRow(tcol)
        for member in parent.members:
            self.titles = [str(member.id),member.name,member.status]
            icol = []
            for t in self.titles:
                item = QStandardItem(t)
                item.setEditable(False)
                icol.append(item)
            self.model.appendRow(icol)
        