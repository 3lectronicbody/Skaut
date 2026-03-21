from PySide6.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton
from models import Users


class EmployeeDetailsWindow(QWidget):
    def __init__(self, database, user, employee, stack):
        super().__init__()
        self.database = database
        self.user = user
        self.employee = employee
        self.stack = stack
        self.setWindowTitle("__data to load__")

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.employee_email_label = QLabel(self)
        self.employee_email_label.setText("__data to load__}")
        self.layout.addWidget(self.employee_email_label, 0, 0)

        self.layout.setRowStretch(1, 1)  # Add stretch to push the back button to the bottom



        last_row = self.layout.rowCount()
        self.back_button = QPushButton(self)
        self.back_button.setText("BACK")
        self.back_button.clicked.connect(self.stack.show_employees_page)
        self.layout.addWidget(self.back_button, last_row + 1, 0)
    def load(self, employee_id):
        with self.database.session() as session:
            emp = session.get(Users, employee_id)
        if emp:
            self.setWindowTitle(f"Details for {emp.name}")
            self.employee_email_label.setText(f"Email: {emp.email}")




