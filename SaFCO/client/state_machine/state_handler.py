class StateHandler(object):
    def __init__(self):
        self.state_data = None
        self.previous_state_callback = None
        self.next_state_callback = None

    def setState(self, state):
        self.state_data = state

    def getState(self):
        return self.state_data

    def startHandlerWork(self):
        pass

    def stopHandlerWork(self):
        pass

    def setStateSwitchCallbacks(self, previous, next):
        self.previous_state_callback = previous
        self.next_state_callback = next
