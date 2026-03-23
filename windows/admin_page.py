from PySide6.QtWidgets import QWidget, QGridLayout


class AdminWindow(QWidget):
    def __init__(self, database, user, stack):
        super().__init__()
        self.database = database
        self.user = user
        self.stack = stack

        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)



