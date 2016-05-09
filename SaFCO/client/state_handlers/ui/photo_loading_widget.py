#!/usr/bin/python3
from PyQt5.QtWidgets import  (QHBoxLayout, QVBoxLayout, QPushButton, QWidget,
                              QScrollArea, QFileDialog, QMessageBox)
from PyQt5.QtGui import QColor
from state_handlers.ui.custom_widgets import QViewer, QToolbar, QImageArea
import constants


class QPhotoLoadingWidget(QWidget):
    def __init__(self, data, complete, back):
        QWidget.__init__(self)
        self.initUI(complete, back)
        self.data = data
        self.image_area = None
           
    def initUI(self, complete, back):
        self.completeButtonClick = complete
        self.backButtonClick = back
    
        main_layout = QHBoxLayout()
         
        self.photo_load_button = QPushButton("Load photo")
        self.complete_button = QPushButton("Complete")
        self.back_button = QPushButton("Back")
        
        self.photo_load_button.clicked.connect(self.loadPhotoDialog)
        
        if self.completeButtonClick != None:
            self.complete_button.clicked.connect(self.nextState)
        if self.backButtonClick != None:
            self.back_button.clicked.connect(self.backButtonClick)
        
        toolbar = QToolbar()
        toolbar.addWidgetToToolbar(self.photo_load_button)
        toolbar.addWidgetToToolbar(self.complete_button)
        toolbar.addWidgetToToolbar(self.back_button)
        toolbar.addStretch(1)
                
        self.viewer = QViewer()
        viewer_scroll = QScrollArea()
        viewer_scroll.setWidget(self.viewer)
        viewer_scroll.setWidgetResizable(True)
        
        main_layout.addWidget(toolbar)
        main_layout.addWidget(viewer_scroll)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)
        
    def loadPhotoDialog(self):
        image_path = QFileDialog.getOpenFileName(self, 'Load image', '/home', 
            "Image files (*jpg *.bmp *.gif *.png)")
        self.data.image_path = image_path[0]
        self.image_area = QImageArea()
        self.image_area.loadImage(self.data.image_path)
        self.viewer.setView(self.image_area)
        
    def nextState(self):
        if self.image_area == None:
             QMessageBox.warning(self, "Photo required.", "Pleace, load photo before continue.")       
        else:
            self.completeButtonClick()
            
    def getState(self):
        if self.image_area != None:
            self.data.image_width = self.image_area.getImageWidth()
            self.data.image_height = self.image_area.getImageHeight()
        return self.data
            
            
if __name__ == '__main__':
    pass