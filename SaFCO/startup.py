from PyQt5.QtWidgets import QApplication
from state_machine.state_data import StateData
from custom_state_pool import CustomStatePool
import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)
    state_pool = CustomStatePool()
    state = StateData()
    
    state.image_width = 800
    state.image_height = 700
    state.image_url = "scheme.jpg"
    
    state_pool.configureStatePool()
    state_pool.start(state)
    
    sys.exit(app.exec_())