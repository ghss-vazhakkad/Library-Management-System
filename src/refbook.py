import sys
from PyQt5 import uic;
from PyQt5.QtWidgets import *;


class RefBook(QDialog):
    def __init__(self):
        super(RefBook, self).__init__()
        uic.loadUi('res/refbook.ui', self)
        self.show()
