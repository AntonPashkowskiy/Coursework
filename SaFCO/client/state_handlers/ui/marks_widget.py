#!/usr/bin/python3
from PyQt5.QtWidgets import  (QHBoxLayout, QVBoxLayout, QPushButton, QWidget,
                              QColorDialog, QScrollArea)
from PyQt5.QtGui import QColor
from state_handlers.ui.custom_widgets import QMarksArea, QViewer, QToolbar
import constants


class QMarksWidget(QWidget):
    def __init__(self, data, complete, back):
        QWidget.__init__(self)
        self.initUI(data, complete, back)
           
    def initUI(self, data, complete, back):
        self.completeButtonClick = complete
        self.backButtonClick = back
    
        main_layout = QHBoxLayout()
         
        self.select_color_button = QPushButton("Choose color of marks")
        self.remove_mode_button = QPushButton("Remove mode")
        self.remove_mode_button.setCheckable(True)
        self.complete_button = QPushButton("Complete")
        self.back_button = QPushButton("Back")
        
        self.select_color_button.clicked.connect(self.showColorSelectionDialog)
        self.remove_mode_button.clicked[bool].connect(self.toggleRemoveMode)
        
        if self.completeButtonClick != None:
            self.complete_button.clicked.connect(self.completeButtonClick)
        if self.backButtonClick != None:
            self.back_button.clicked.connect(self.backButtonClick)
        
        toolbar = QToolbar()
        toolbar.addWidgetToToolbar(self.select_color_button)
        toolbar.addWidgetToToolbar(self.remove_mode_button)
        toolbar.addWidgetToToolbar(self.complete_button)
        toolbar.addWidgetToToolbar(self.back_button)
        toolbar.addStretch(1)
        
        self.markable_area = QMarksArea()
        self.markable_area.setMaximumSize(data.image_width, data.image_height)
        self.markable_area.loadImage(data.image_path)
        self.markable_area.setBrushColor(QColor(constants.defaultBrushColor))       
        
        viewer = QViewer()
        viewer.setView(self.markable_area)
        viewer_scroll = QScrollArea()
        viewer_scroll.setWidget(viewer)
        viewer_scroll.setWidgetResizable(True)
        
        main_layout.addWidget(toolbar)
        main_layout.addWidget(viewer_scroll)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)
    
    def showColorSelectionDialog(self):
        newColor = QColorDialog.getColor() 
        if newColor.isValid():
            self.markable_area.setBrushColor(newColor)
            
    def toggleRemoveMode(self, pressed):
        if pressed:
            self.markable_area.setRemoveMode()
        else:
            self.markable_area.resetRemoveMode()
    
    def getMarks(self):
        return self.markable_area.getMarks()
            
            
if __name__ == '__main__':
    pass