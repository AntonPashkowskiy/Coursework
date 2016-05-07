#!/usr/bin/python3
import sys
from PyQt5.QtWidgets import  (QMainWindow, QApplication, QHBoxLayout, 
                              QVBoxLayout, QPushButton, QWidget,
                              QColorDialog, QScrollArea)
from PyQt5.QtGui import QColor
from custom_widgets import QMarksArea, QViewer, QToolbar
import constants


class StartWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.initUI()
           
    def initUI(self):
        main_layout = QHBoxLayout()
         
        self.select_color_button = QPushButton("Choose color of marks")
        self.remove_mode_button = QPushButton("Remove mode")
        self.remove_mode_button.setCheckable(True)
        self.complete_button = QPushButton("Complete")
        
        self.select_color_button.clicked.connect(self.showColorSelectionDialog)
        self.remove_mode_button.clicked[bool].connect(self.toggleRemoveMode)
        
        toolbar = QToolbar()
        toolbar.addWidgetToToolbar(self.select_color_button)
        toolbar.addWidgetToToolbar(self.remove_mode_button)
        toolbar.addWidgetToToolbar(self.complete_button)
        toolbar.addStretch(1)
        
        self.markable_area = QMarksArea()
        self.markable_area.setMaximumSize(800, 700)
        self.markable_area.loadImage('scheme.jpg')
        self.markable_area.setBrushColor(QColor(constants.defaultBrushColor))       
        
        viewer = QViewer()
        viewer.setView(self.markable_area)
        viewer_scroll = QScrollArea()
        viewer_scroll.setWidget(viewer)
        viewer_scroll.setWidgetResizable(True)
        
        main_layout.addWidget(toolbar)
        main_layout.addWidget(viewer_scroll)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        
        self.setCentralWidget(main_widget)
        self.setMinimumSize(300, 300)
        self.setWindowTitle('Marks')
        self.showMaximized()
    
    def showColorSelectionDialog(self):
        newColor = QColorDialog.getColor() 
        if newColor.isValid():
            self.markable_area.setBrushColor(newColor)
            
    def toggleRemoveMode(self, pressed):
        if pressed:
            self.markable_area.setRemoveMode()
        else:
            self.markable_area.resetRemoveMode()


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = StartWindow()
    sys.exit(app.exec_())