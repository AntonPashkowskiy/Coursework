#!/usr/bin/python3
from state_machine.state_handler import StateHandler
from state_handlers.ui.drilling_widget import QDrillingWidget
from state_handlers.utils.calculating_utils import translate_coordinates
from state_handlers.ui.main_window import set_widget
from com import com_provider
from functools import cmp_to_key
from pprint import pprint


class DrillingHandler(StateHandler):
    def __init__(self):
        StateHandler.__init__(self)
        self.widget = None

    def startHandlerWork(self):
        self.widget = QDrillingWidget(self.state_data, self.next_state_callback, self.previous_state_callback)
        self.widget.setDrillingCompleteState(False)
        set_widget(self.widget, "Drilling")
        self.widget.showInformationMessage("Drilling", "Drilling in progress. Please, wait.")

        if self.state_data.coordinates is not None:
            print('circ:', self.state_data.circuit_coordinates)
            print('image: ', self.state_data.image_coordinates)
            print('scale', self.state_data.scale)
            print('points before:')
            pprint(self.state_data.coordinates)

            scale = self.state_data.scale
            circuit_coordinates = self.state_data.circuit_coordinates
            image_coordinates = self.state_data.image_coordinates
            points = [translate_coordinates(circuit_coordinates, image_coordinates, scale, point)
                      for point in self.state_data.coordinates]
            # points = self.sortCoordinatesForDrilling(points)

            print('points after:')
            pprint(points)

            try:
                pass
                com_provider.open_driller_port()
                for point in points:
                    com_provider.move_drill(point[0], point[1])  # !!!
                    com_provider.touch_circuit()  # !!!
                com_provider.close_driller_port()
            except RuntimeError as error:
                self.widget.showErrorMessage("Error", str(error))
        self.widget.setDrillingCompleteState(True)

    def stopHandlerWork(self):
        self.widget.hide()

    def sortCoordinatesForDrilling(self, points):
        def compare(left, right):
            left_x, left_y = left
            right_x, right_y = right
            x_diff = left_x - right_x

            if x_diff == 0:
                return left_y - right_y
            return x_diff

        return sorted(points, key=cmp_to_key(compare))


if __name__ == '__main__':
    pass
