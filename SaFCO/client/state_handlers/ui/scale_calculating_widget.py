#!/usr/bin/python3
from PyQt5.QtWidgets import  (QHBoxLayout, QVBoxLayout, QPushButton, QWidget,
                              QColorDialog, QScrollArea, QMessageBox)
from PyQt5.QtGui import QColor
from PyQt5 import QtCore
from state_handlers.ui.custom_widgets import QMarksArea, QViewer, QToolbar
from com import constants as device_constants
from com.drill_positioning import DrillPositioningManager
import constants


class QScaleCalculatingWidget(QWidget):
    def __init__(self, data, complete, back):
        QWidget.__init__(self)
        self.initUI(data, complete, back)
        self.is_drill_positioning_mode = False
        self.drill_positioning_manager = None
        self.coordinates_from_drill = []
           
    def initUI(self, data, complete, back):
        self.completeButtonClick = complete
        self.backButtonClick = back
    
        main_layout = QHBoxLayout()
         
        self.touch_circuit_button = QPushButton("Touch circuit")
        self.drill_mode_button = QPushButton("Drill positioning mode")
        self.drill_mode_button.setCheckable(True)
        self.remove_mode_button = QPushButton("Remove mode")
        self.remove_mode_button.setCheckable(True)
        self.get_coordinate_button = QPushButton("Get coordinate from drill")
        self.complete_button = QPushButton("Complete")
        self.back_button = QPushButton("Back")
        
        self.touch_circuit_button.clicked.connect(self.touchCircuit)
        self.get_coordinate_button.clicked.connect(self.getCoordinateFromDrill)
        self.remove_mode_button.clicked[bool].connect(self.toggleRemoveMode)
        self.drill_mode_button.clicked[bool].connect(self.toggleDrillPositioningMode)
        
        if self.completeButtonClick != None:
            self.complete_button.clicked.connect(self.handleCompleteButtonClick)
        if self.backButtonClick != None:
            self.back_button.clicked.connect(self.backButtonClick)
        
        toolbar = QToolbar()
        toolbar.addWidgetToToolbar(self.drill_mode_button)
        toolbar.addWidgetToToolbar(self.touch_circuit_button)
        toolbar.addWidgetToToolbar(self.get_coordinate_button)
        toolbar.addWidgetToToolbar(self.remove_mode_button)
        toolbar.addWidgetToToolbar(self.complete_button)
        toolbar.addWidgetToToolbar(self.back_button)
        toolbar.addStretch(1)
        
        self.markable_area = QMarksArea()
        self.markable_area.setMaximumSize(data.image_width, data.image_height)
        self.markable_area.loadImage(data.image_path)
        self.markable_area.setMarksCountLimit(2)
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
        
    def getCoordinatesFromImage(self):
        return self.markable_area.getMarks()
        
    def getCoordinatesFromDrill(self):
        return self.coordinates_from_drill.copy()
        
    def touchCircuit(self):
        if self.is_drill_positioning_mode:
            self.drill_positioning_manager.touchToCircuit()
            
    def toggleRemoveMode(self, pressed):
        if pressed:
            self.markable_area.setRemoveMode()
        else:
            self.markable_area.resetRemoveMode()
        
    def toggleDrillPositioningMode(self, pressed):
        try:
            if self.is_drill_positioning_mode:
                self.drill_positioning_manager.disconnectDrill()
                self.is_drill_positioning_mode = False
            else:
                if self.drill_positioning_manager == None:
                    self.drill_positioning_manager = DrillPositioningManager()
                self.drill_positioning_manager.connectWithDrill()        
                self.is_drill_positioning_mode = True
        except RuntimeError as error:
            QMessageBox.critical(self, "Error", str(error))
                    
    def getCoordinateFromDrill(self):
        if self.drill_positioning_manager != None:
            coordinate = self.drill_positioning_manager.getDrillCoordinate()
            if coordinate != None:
                self.coordinates_from_drill.append(coordinate)
            
    def handleCompleteButtonClick(self):
        marks = self.getCoordinatesFromImage()
        
        if len(self.coordinates_from_drill) >= 2 and len(marks) >= 2:
            self.completeButtonClick()
        else:
            QMessageBox.warning(self, "Scale calculating error", 
                "Not enought coordinates for scale calcualting")    
    
    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return
        try:
            if self.is_drill_positioning_mode:
                if event.key() == QtCore.Qt.Key_W:
                    self.drill_positioning_manager.startPositioning(device_constants.top_direction)
                elif event.key() == QtCore.Qt.Key_S:
                    self.drill_positioning_manager.startPositioning(device_constants.bottom_direction)
                elif event.key() == QtCore.Qt.Key_A:
                    self.drill_positioning_manager.startPositioning(device_constants.left_direction)
                elif event.key() == QtCore.Qt.Key_D:
                    self.drill_positioning_manager.startPositioning(device_constants.right_direction)
                elif event.key() == QtCore.Qt.Key_Escape:
                    self.drill_positioning_manager.stopPositioning()
        except RuntimeError as error:
            QMessageBox.critical(self, "Error", str(error))
            
            
if __name__ == '__main__':
    pass
