#!/usr/bin/python3
from state_machine.state_handler import StateHandler
from state_handlers.ui.marks_widget import QMarksWidget
from state_handlers.ui.main_window import set_widget


class MarksAddingHandler(StateHandler):
    def __init__(self):
        StateHandler.__init__(self)
        self.widget = None
        
    def getState(self):
        if (self.widget != None):
            self.state_data.marks = self.widget.getMarks()
        return self.state_data
    
    def startHandlerWork(self):
        self.widget = QMarksWidget(self.state_data, self.next_state_callback, self.previous_state_callback)
        set_widget(self.widget, "Marks adding")
    
    def stopHandlerWork(self):
        self.widget.hide()    


if __name__ == '__main__':
    pass
