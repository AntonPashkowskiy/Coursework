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
        self.setMinimumWidth(constants.toolbarMinWidth)
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
        self.viewer_layout = QVBoxLayout()
        horizontal_layout = QHBoxLayout()
        
        viewer_widget_palette = QPalette()
        viewer_widget_palette.setColor(QPalette.Background, QColor(constants.defaultViewerColor))
        self.setAutoFillBackground(True)
        self.setPalette(viewer_widget_palette)
        
        horizontal_layout.addLayout(self.viewer_layout)
        self.setLayout(horizontal_layout)
    
    def setView(self, view):
        self.viewer_layout.addStretch(1)
        self.viewer_layout.addWidget(view)
        self.viewer_layout.addStretch(1)
    
class QMarkablePicture(QLabel):
    def __init__(self, parent = None):
        QLabel.__init__(self, parent)
        self.initBrush()
        self.marks = []
        self.is_marks_count_limited = False
        self.marks_count_limit = 0
            
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
        if self.__isAbleDrawMark():
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
    
    def setMarksCountLimit(self, limit):
        self.is_marks_count_limited = True
        self.marks_count_limit = limit
        
    def __isAbleDrawMark(self):
        limit_enabled_condition = self.is_marks_count_limited and (len(self.marks) < self.marks_count_limit)
        limit_disabled_condition = not self.is_marks_count_limited
        return limit_enabled_condition or limit_disabled_condition
    
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
        
    def setMarksCountLimit(self, limit):
        self.markable_picture.setMarksCountLimit(limit)
    
    def drawMark(self, position):
        self.markable_picture.drawMark(position)
    
    def setRemoveMode(self):
        self.remove_mode = True
    
    def resetRemoveMode(self):
        self.remove_mode = False
    
    def removeMark(self, position):
        self.markable_picture.removeMark(position)
    
    def getMarks(self):
        marks = self.markable_picture.getMarks()
        return [(mark.x(), mark.y()) for mark in marks]
        

class QImageArea(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)   
    
    def loadImage(self, path):
        self.picture_label = QLabel(self)
        hbox = QHBoxLayout(self)
        self.picture = QPixmap(path)
                
        self.picture_label.setPixmap(self.picture)
        hbox.addWidget(self.picture_label)
        hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hbox)
    
    def getImageWidth(self):
        return self.picture.width()
    
    def getImageHeight(self):
        return self.picture.height()
    
    
if __name__ == '__main__':
    pass
