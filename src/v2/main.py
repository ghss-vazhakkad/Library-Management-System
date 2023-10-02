import threading
import time
import sys
import random
import webview

class Api:
    def __init__(self):
        pass
    def contact(self,str):
        print(str)
        return str




if __name__ == '__main__':
    api = Api()
    window = webview.create_window('Library Management System', "../../assets/www/index.html", js_api=api)
    window.fullscreen = True
    webview.start()
    
    