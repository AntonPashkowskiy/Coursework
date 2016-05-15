from PyQt5.QtWidgets import QMainWindow

main_window = None


class QMainApplicationWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        self.setMinimumSize(300, 300)
        self.setWindowTitle('Title')
        self.showMaximized()


def set_widget(widget, title="Title"):
    global main_window
    if main_window is None:
        main_window = QMainApplicationWindow()
    main_window.setCentralWidget(widget)
    main_window.setWindowTitle(title)
