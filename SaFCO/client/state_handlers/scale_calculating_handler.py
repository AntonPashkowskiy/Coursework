#!/usr/bin/python3
from state_machine.state_handler import StateHandler
from state_handlers.ui.scale_calculating_widget import QScaleCalculatingWidget
from state_handlers.ui.main_window import set_widget
from state_handlers.utils.calculating_utils import calculate_scale


class ScaleCalculatingHandler(StateHandler):
    def __init__(self):
        StateHandler.__init__(self)
        self.widget = None

    def getState(self):
        if self.widget is not None:
            self.state_data.circuit_coordinates = self.widget.getCoordinatesFromDrill()
            self.state_data.image_coordinates = self.widget.getCoordinatesFromImage()
            self.state_data.scale = calculate_scale(self.state_data.circuit_coordinates,
                                                    self.state_data.image_coordinates)
            return self.state_data
        return self.state_data

    def startHandlerWork(self):
        self.widget = QScaleCalculatingWidget(self.state_data, self.next_state_callback,
                                              self.previous_state_callback)
        set_widget(self.widget, "Scale calculating")

    def stopHandlerWork(self):
        self.widget.hide()
