#!/usr/bin/python3
from state_machine.state_handler import StateHandler
from state_handlers.ui.drilling_widget import QDrillingWidget
from state_handlers.utils.calculating_utils import translate_coordinates
from state_handlers.ui.main_window import set_widget
from com import constants
from com import com_provider
from functools import cmp_to_key


class DrillingHandler(StateHandler):
    def __init__(self):
        StateHandler.__init__(self)
        self.widget = None
        
    def startHandlerWork(self):
        self.widget = QDrillingWidget(self.state_data, self.next_state_callback, self.previous_state_callback)
        self.widget.setDrillingCompleteState(False)
        set_widget(self.widget, "Drilling")
        self.widget.showInformationMessage("Drilling", "Drilling in progress. Pleace, wait.")
                    
        if self.state_data.coordinates != None:
            scale = self.state_data.scale
            coordinates = [(coordinate[0] * scale, coordinate[1] * scale) 
                            for coordinate in self.state_data.coordinates]
            translate_cooficient = 1 / constants.steps_on_millimetr
            coordinates = translate_coordinates(coordinates, translate_cooficient)
            coordinates = self.sortCoordinatesForDrilling(coordinates)

            try:
                pass
                com_provider.open_driller_port()
                for coordinate in coordinates:
                    com_provider.drill_circuit(coordinate[0], coordinate[1])                        
                com_provider.close_driller_port()
            except RuntimeError as error:
                self.widget.showErrorMessage("Error", str(error))
        self.widget.setDrillingCompleteState(True)
    
    def stopHandlerWork(self):
        self.widget.hide() 
        
    def sortCoordinatesForDrilling(self, coordinates):
        def compare(left, right):
            left_x, left_y = left
            right_x, right_y = right
            x_diff = left_x - right_x
            
            if x_diff == 0:
                return left_y - right_y
            return x_diff
            
        return sorted(coordinates, key=cmp_to_key(compare))   


if __name__ == '__main__':
    pass