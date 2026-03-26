from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton


class AdminWindow(QWidget):
    def __init__(self, database, user, stack):
        super().__init__()
        self.database = database
        self.user = user
        self.stack = stack

        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)

        self.employees_button = QPushButton("Employees", flat=True)
        self.main_layout.addWidget(self.employees_button, 0, 0)
        self.employees_button.clicked.connect(self.stack.show_employees_page)

        self.back_button = QPushButton("Back")
        self.main_layout.addWidget(self.back_button, 1, 0)
        self.back_button.clicked.connect(self.stack.show_main_page)



