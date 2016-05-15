from state_machine.state_handler import StateHandler
from state_handlers.ui.marks_widget import QMarksWidget
from state_handlers.ui.main_window import set_widget
from state_handlers.utils.calculating_utils import translate_coordinates
import constants


class MarksAddingHandler(StateHandler):
    def __init__(self):
        StateHandler.__init__(self)
        self.widget = None

    def getState(self):
        if (self.widget is not None):
            marks = self.widget.getMarks()
            self.state_data.coordinates = translate_coordinates(marks, constants.pixels_on_millimetr)
        return self.state_data

    def startHandlerWork(self):
        self.widget = QMarksWidget(self.state_data, self.next_state_callback, self.previous_state_callback)
        set_widget(self.widget, "Marks adding")

    def stopHandlerWork(self):
        self.widget.hide()
