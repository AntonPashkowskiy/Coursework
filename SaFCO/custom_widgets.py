#!/usr/bin/python3
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor, QPalette
from PyQt5.QtCore import Qt, QPoint
import constants

class QToolbar(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.initUI()
    
    def initUI(self):
        self.tools_layout = QVBoxLayout()
        self.setMaximumWidth(constants.toolbarMaxWidth)
        self.setLayout(self.tools_layout)
    
    def addWidgetToToolbar(self, widget):
        self.tools_layout.addWidget(widget)
        
    def addStretch(self, stretch):
        self.tools_layout.addStretch(stretch)


class QViewer(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.initUI()
        
    def initUI(self):
        self.viewer_layout = QHBoxLayout()
        viewer_widget_palette = QPalette()
        viewer_widget_palette.setColor(QPalette.Background, QColor(constants.defaultViewerColor))
        self.setAutoFillBackground(True)
        self.setPalette(viewer_widget_palette)
        self.setLayout(self.viewer_layout)
    
    def setView(self, view):
        self.viewer_layout.addWidget(view)
    
    
class QMarkablePicture(QLabel):
    def __init__(self, parent = None):
        QLabel.__init__(self, parent)
        self.initBrush()
        self.marks = []
            
    def initBrush(self):
        self.brush = QBrush(Qt.SolidPattern)
        self.brush.setColor(QColor(constants.defaultBrushColor))        
           
    def paintEvent(self, e):
        QLabel.paintEvent(self, e)
        painter = QPainter()
        painter.begin(self)
        painter.setBrush(self.brush)
        for mark in self.marks:
            painter.drawEllipse(mark, constants.ellipsWidth, constants.ellipsHeight)
        painter.end()
        
    def setBrushColor(self, color):
        self.brush.setColor(color)    
        
    def drawMark(self, mark):
        self.marks.append(mark)
        self.update()
    
    def removeMark(self, mark):
        for painted_mark in self.marks:
            if self.__isApproximatelyEqual(mark, painted_mark, constants.epsilon):
                self.marks.remove(painted_mark)
                break
        self.update()
        
    def getMarks(self):
        return self.marks.copy()
    
    def __isApproximatelyEqual(self, firstMark, secondMark, epsilon):
        full_equality = firstMark == secondMark
            
        x_top_limit = (firstMark.x() + epsilon) >= secondMark.x()
        x_bottom_limit = (firstMark.x() - epsilon) <= secondMark.x()
        x_equality = x_top_limit and x_bottom_limit
            
        y_top_limit = (firstMark.y() + epsilon) >= secondMark.y()
        y_bottom_limit = (firstMark.y() - epsilon) <= secondMark.y()
        y_equality = y_top_limit and y_bottom_limit

        return full_equality or (x_equality and y_equality)    


class QMarksArea(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.remove_mode = False
        
    def mousePressEvent(self, e):
        if self.remove_mode:
            self.removeMark(e.pos())
        else:
            self.drawMark(e.pos())    
        
    def loadImage(self, path):
        self.markable_picture = QMarkablePicture(self)
        hbox = QHBoxLayout(self)
        picture = QPixmap(path)
        
        if picture.width() > self.maximumWidth():
            picture = picture.scaledToWidth(self.maximumWidth())
        if picture.height() > self.maximumHeight():
            picture = picture.scaledToHeight(self.maximumHeight())
        
        self.markable_picture.setPixmap(picture)
        hbox.addWidget(self.markable_picture)
        hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hbox)
          
    def setBrushColor(self, color):
        self.markable_picture.setBrushColor(color)
    
    def drawMark(self, position):
        self.markable_picture.drawMark(position)
    
    def setRemoveMode(self):
        self.remove_mode = True
    
    def resetRemoveMode(self):
        self.remove_mode = False
    
    def removeMark(self, position):
        self.markable_picture.removeMark(position)
    
    def getMarks(self):
        return self.markable_picture.getMarks()
    
    
if __name__ == '__main__':
    pass