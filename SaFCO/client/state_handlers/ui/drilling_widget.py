#!/usr/bin/python3
from PyQt5.QtWidgets import  (QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QScrollArea, QMessageBox)
from PyQt5.QtGui import QColor
from state_handlers.ui.custom_widgets import QMarksArea, QViewer, QToolbar
import constants


class QDrillingWidget(QWidget):
    def __init__(self, data, complete, back):
        QWidget.__init__(self)
        self.initUI(data, complete, back)
        self.is_drilling_completed = False
        
           
    def initUI(self, data, complete, back):
        self.completeButtonClick = complete
        self.backButtonClick = back
    
        main_layout = QHBoxLayout()
        
        self.complete_button = QPushButton("Complete")
        self.back_button = QPushButton("Back")
               
        if self.completeButtonClick != None:
            self.complete_button.clicked.connect(self.handleCompleteButtonClick)
        if self.backButtonClick != None:
            self.back_button.clicked.connect(self.handlerBackButtonClick)
        
        toolbar = QToolbar()
        toolbar.addWidgetToToolbar(self.complete_button)
        toolbar.addWidgetToToolbar(self.back_button)
        toolbar.addStretch(1)
            
        viewer = QViewer()
        viewer_scroll = QScrollArea()
        viewer_scroll.setWidget(viewer)
        viewer_scroll.setWidgetResizable(True)
        
        main_layout.addWidget(toolbar)
        main_layout.addWidget(viewer_scroll)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)
    
    def handleCompleteButtonClick(self):
        if self.is_drilling_completed:
            self.completeButtonClick()
        else:
            QMessageBox.warning(self, "Warning", "Drilling is not completed. Pleace, wait.")
    
    def handlerBackButtonClick(self):
        if self.is_drilling_completed:
            self.backButtonClick()
        else:
            QMessageBox.warning(self, "Warning", "Drilling is not completed. Pleace, wait.")
        
    def setDrillingCompleteState(self, state):
        self.is_drilling_completed = state
        
    def showErrorMessage(self, title, error):
        if title != None and error != None:
            QMessageBox.critical(self, title, error)
        
    def showInformationMessage(self, title, message):
        if title != None and message != None:
            QMessageBox.information(self, title, message)    
            
            
if __name__ == '__main__':
    pass