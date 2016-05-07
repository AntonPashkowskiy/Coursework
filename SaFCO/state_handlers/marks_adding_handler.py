#!/usr/bin/python3
from state_machine.state_handler import StateHandler
from state_handlers.ui.marks_window import QMarksWindow


class MarksAddingHandler(StateHandler):
    def __init__(self):
        StateHandler.__init__(self)
        self.window = None
        
    def getState(self):
        if (self.window != None):
            self.state_data.marks = self.window.getMarks()
        return self.state_data
    
    def startHandlerWork(self):
        self.window = QMarksWindow(self.state_data, self.next_state_callback, self.previous_state_callback)
    
    def stopHandlerWork(self):
        self.window.hide()    


if __name__ == '__main__':
    pass
