#!/usr/bin/python3
from state_machine.state_handler import StateHandler
from state_handlers.ui.photo_loading_widget import QPhotoLoadingWidget
from state_handlers.ui.main_window import set_widget


class PhotoLoadingHandler(StateHandler):
    def __init__(self):
        StateHandler.__init__(self)
        self.widget = None

    def getState(self):
        if self.widget is not None:
            return self.widget.getState()
        return self.state_data

    def startHandlerWork(self):
        self.widget = QPhotoLoadingWidget(self.state_data, self.next_state_callback,
                                          self.previous_state_callback)
        set_widget(self.widget, "Photo loading")

    def stopHandlerWork(self):
        self.widget.hide()
