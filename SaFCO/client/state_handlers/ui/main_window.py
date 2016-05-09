#!/usr/bin/python3
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QColor
from state_handlers.ui.custom_widgets import QMarksArea, QViewer, QToolbar
import constants


class QMainApplicationWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.initUI()
           
    def initUI(self):
        self.setMinimumSize(300, 300)
        self.setWindowTitle('Title')
        self.showMaximized()
        

main_window = None

def set_widget(widget, title="Title"):
    global main_window
    
    if main_window == None:
        main_window = QMainApplicationWindow()
    main_window.setCentralWidget(widget)
    main_window.setWindowTitle(title)
    
            
if __name__ == '__main__':
    pass