#!/usr/bin/python3

class StatePool(object):
    def __init__(self):
        self.state_handlers = []
        self.current_state_index = 0
    
    def __addHandlerToPool(self, handler):
        self.state_handlers.append(handler)
        
    def __previousStateHandler(self):
        if len(self.state_handlers) == 0:
            raise Exception("State pool error. Handlers are not defined")
    
        if self.current_state_index != 0:
            return self.state_handlers[self.current_state_index - 1]
        else:
            return self.state_handlers[len(self.state_handlers) - 1]
    
    def __nextStateHandler(self):
        if len(self.state_handlers) == 0:
            raise Exception("State pool error. Handlers are not defined")
            
        if self.current_state_index != len(self.state_handlers) - 1:
            return self.state_handlers[self.current_state_index + 1]
        else:
            return selfstate_handlers[0]
    
    def __decrementStateIndex(self):
        if self.current_state_index != 0:
            self.current_state_index -= 1
        else:
            self.current_state_index = len(self.state_handlers) - 1
    
    def __incrementStateIndex(self):
        if self.current_state_index != len(self.current_state_index) - 1:
            self.current_state_index += 1
        else:
            self.current_state_index = 0
            
    def __switchHandlers(self, current_handler, new_handler):
        if current_handler == None or new_handler == None:
            raise Exception("State pool error. Undefined handlers.")
        state = current_handler.getState()
        new_handler.setState(state)
        current_handler.stopHandlerWork()
        new_handler.startHandlerWork()     
        
    def previousState(self):
        try:
            if len(self.state_handlers) > 0 and self.current_state_index != 0:
                current_handler = self.state_handlers[self.current_state_index]
                new_handler = self.__previousStateHandler()
                
                self.__switchHandlers(current_handler, new_handler)
                self.__decrementStateIndex()
        except Exception as unexpected_exception:
            print(unexpected_exception)
    
    def nextState(self):
        try:
            if len(self.state_handlers) > 0:
                if self.current_state_index == len(self.state_handlers) - 1:
                    return
                else:
                    current_handler = self.state_handlers[self.current_state_index]
                    new_handler = self.__nextStateHandler()
                    
                    self.__switchHandlers()
                    self.__incrementStateIndex()
        except Exception as unexpected_exception:
            print(unexpected_exception)
    
    def configurePool(self):
        pass


if __name__ == '__main__':
    pass