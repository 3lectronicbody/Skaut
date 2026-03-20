from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton

class EmployeesWindow(QWidget):
    def __init__(self, database, user, stack):
        super().__init__()
        self.database = database
        self.user = user
        self.stack = stack

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.setWindowTitle("Employees Page")

        self.reload_layout = QGridLayout()
        self.layout.addLayout(self.reload_layout, 0, 0)

        self.reload()



    def reload(self):
        # Clear existing layout if it exists
        while self.reload_layout.count():
            child = self.reload_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


        # Example: Add a button to go back to admin page
        back_button = QPushButton("Back to Admin Page")
        self.reload_layout.addWidget(back_button, 0, 0)
        back_button.clicked.connect(self.stack.show_admin_page)

