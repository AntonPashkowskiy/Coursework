#!/usr/bin/python3
from com import com_provider, constants

class DrillPositioningManager(object):
    def __init__(self):
        object.__init__(self)
        self.stop_signal = False
        self.drill_is_connected = False
    
    def moveTo(self, direction):
        if self.drill_is_connected:
            x, y = (0, 0)
            #x, y = com_provider.get_drill_coordinates()
            drill_step = constants.steps_on_millimetr / 2
                
            while not self.stop_signal:
                if direction == constants.left_direction:
                    x -= drill_step                     
                elif direction == constants.right_direction:
                    x += drill_step
                elif direction == constants.top_direction:
                    y += drill_step
                elif direction == constants.bottom_direction:
                    y -= drill_step
                print("move_drill " + str(x) + " " + str(y))
                #com_provider.move_drill(x, y)                
    
    def getDrillCoordinate(self):
        if self.drill_is_connected:
            return com_provider.get_drill_coordinates()
        else:
            return None
    
    def stop(self):
        self.stop_signal = True
        
    def connectWithDrill(self):
        self.drill_is_connected = True
        #if not self.drill_is_connected:
            #self.drill_is_connected = com_provider.open_driller_port()
        
    def disconnectDrill(self):
        self.drill_is_connected = False
        #if self.drill_is_connected:
            #com_provider.close_driller_port()
            #self.drill_is_connected = False                