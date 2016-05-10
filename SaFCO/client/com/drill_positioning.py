#!/usr/bin/python3
from com import com_provider, constants
import multiprocessing
import time


class DrillPositioningManager(object):
    def __init__(self):
        object.__init__(self)
        self.worker = None
        self.drill_is_connected = False
    
    def __moveTo(self, direction):
        if self.drill_is_connected:
            x, y = com_provider.get_drill_coordinates()
            drill_step = constants.steps_on_millimetr / 2
                
            while True:
                if direction == constants.left_direction:
                    x -= drill_step                     
                elif direction == constants.right_direction:
                    x += drill_step
                elif direction == constants.top_direction:
                    y += drill_step
                elif direction == constants.bottom_direction:
                    y -= drill_step
                
                if not com_provider.move_drill(x, y):
                    break                
    
    def getDrillCoordinate(self):
        if self.drill_is_connected:
            return com_provider.get_drill_coordinates()
        else:
            return None
    
    def touchToCircuit(self):
        if self.drill_is_connected:
            com_provider.touch_circuit()
            
    def startPositioning(self, direction):
        if self.worker != None:
            self.worker.terminate()
        self.worker = multiprocessing.Process(target=self.__moveTo, args=(direction,))
        self.worker.start()
    
    def stopPositioning(self):
        if self.worker != None:
            self.worker.terminate()
        
    def connectWithDrill(self):
        if not self.drill_is_connected:
            self.drill_is_connected = com_provider.open_driller_port()
        
    def disconnectDrill(self):
        self.drill_is_connected = False
        if self.drill_is_connected:
            com_provider.close_driller_port()
            self.drill_is_connected = False                