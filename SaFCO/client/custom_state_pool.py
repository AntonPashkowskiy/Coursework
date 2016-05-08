from state_machine.state_pool import StatePool
from state_handlers.marks_adding_handler import MarksAddingHandler

class CustomStatePool(StatePool):
    def __init__(self):
        StatePool.__init__(self)
    
    def configureStatePool(self):
        self.addHandlerToStatePool(MarksAddingHandler())
