from functools import partial

from PySide6.QtWidgets import QWidget, QGridLayout, QToolButton, QPushButton
from models import Users

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
        with self.database.session() as session:
            employees = session.query(Users).all()
            for index, emp in enumerate(employees):
                email_label = QPushButton(emp.email, flat=True)
                email_label.setStyleSheet("border: 2px")
                self.reload_layout.addWidget(email_label, index, 0)
                email_label.clicked.connect(partial(self.stack.show_employee_details_page, emp.id))

        self.reload_layout.setRowStretch(index+1,1)
        back_button = QPushButton("Back to Admin Page")
        self.reload_layout.addWidget(back_button, index+ 2, 0)
        back_button.clicked.connect(self.stack.show_admin_page)

