from PySide6.QtWidgets import QWidget, QGridLayout


class AdminWindow(QWidget):
    def __init__(self, database, user, stack):
        super().__init__()
        self.database = database
        self.user = user
        self.stack = stack



        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.setWindowTitle("Admin Page")


