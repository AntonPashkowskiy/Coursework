#!/usr/bin/env python3
from PyQt5.QtWidgets import QApplication
from state_machine.state_data import StateData
from custom_state_pool import CustomStatePool
import sys


def main():
    app = QApplication(sys.argv)
    state_pool = CustomStatePool()
    state = StateData()
    state_pool.configureStatePool()
    state_pool.start(state)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
