from state_machine.state_pool import StatePool
from state_handlers.marks_adding_handler import MarksAddingHandler
from state_handlers.photo_loading_handler import PhotoLoadingHandler
from state_handlers.scale_calculating_handler import ScaleCalculatingHandler
from state_handlers.drilling_handler import DrillingHandler

class CustomStatePool(StatePool):
    def __init__(self):
        StatePool.__init__(self)
    
    def configureStatePool(self):
        self.addHandlerToStatePool(PhotoLoadingHandler())
        self.addHandlerToStatePool(ScaleCalculatingHandler())
        self.addHandlerToStatePool(MarksAddingHandler())
        self.addHandlerToStatePool(DrillingHandler())
