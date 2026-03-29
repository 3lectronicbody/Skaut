from functools import partial

from PySide6.QtWidgets import QWidget, QGridLayout, QToolButton, QPushButton, QTableWidget, QComboBox
from models import Users, Role
from helper import confirmation_message

class EmployeesWindow(QWidget):
    def __init__(self, database, user, stack):
        super().__init__()
        self.database = database
        self.user = user
        self.stack = stack

        self.combos = {}

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
                email_label = QPushButton(emp.email, flat=False)
                self.reload_layout.addWidget(email_label, index, 0)
                email_label.clicked.connect(partial(self.stack.show_employee_details_page, emp.id))


                role_combo = QComboBox()
                role_combo.addItems([role.value for role in Role])
                self.reload_layout.addWidget(role_combo, index, 1)
                role_combo.setCurrentText(emp.role)

                self.combos[emp.id] = role_combo



            # Columns relative stretch
            self.reload_layout.setColumnStretch(0,3)
            self.reload_layout.setColumnStretch(1,1)

        self.reload_layout.setRowStretch(index+1,1)

        back_button = QPushButton("Back to Admin Page")
        self.reload_layout.addWidget(back_button, index + 2, 0)
        back_button.clicked.connect(self.stack.show_admin_page)

        save_button = QPushButton("Save Changes")
        save_button.setStyleSheet("background-color: green;")
        self.reload_layout.addWidget(save_button, index + 2 , 1)
        save_button.clicked.connect(self.save_button_function)

    def save_button_function(self):
        message = confirmation_message('Do You want to save changes?')
        if message:
            updated_roles = {idx : combo.currentText() for idx, combo in self.combos.items()}
            with self.database.session() as session:

                for idx, role in updated_roles.items():
                    user = session.get(Users, idx)
                    if user.role != role:
                        user.role = role
                session.commit()
                self.stack.show_admin_page()














