from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton


class AdminWindow(QWidget):
    def __init__(self, database, user, stack):
        super().__init__()
        self.database = database
        self.user = user
        self.stack = stack



        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.setWindowTitle("Admin Page")

        self.employees_button= QPushButton("Employees")
        self.layout.addWidget(self.employees_button, 0, 0)
        self.employees_button.clicked.connect(self.employees_button_function)

        self.layout.setRowStretch(1, 1)
        self.back_button = QPushButton("Back to Main Menu")
        self.layout.addWidget(self.back_button, 2, 0)
        self.back_button.clicked.connect(self.stack.show_main_page)

    def employees_button_function(self):
        self.stack.show_employees_page()


