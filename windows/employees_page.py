from functools import partial

from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QComboBox
from models import Users, Role

from database import Database


class EmployeesWindow(QWidget):
    def __init__(self, database: Database, stack):
        super().__init__()

        self.database = database
        self.stack = stack

        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)


        self.data_layout = QGridLayout()
        self.main_layout.addLayout(self.data_layout, 0, 0)

        self.back_button = QPushButton("Back")
        self.main_layout.addWidget(self.back_button, 1, 0)
        self.back_button.clicked.connect(lambda: self.stack.show_admin_page())
        self.refresh_data()

    def refresh_data(self):

        counter = 0
        with self.database.session() as session:
            table = session.query(Users).all()

            for index, user in enumerate(table):
                name_label = QLabel(self)
                name_label.setText(user.name if not None else "")
                self.data_layout.addWidget(name_label, index, 0)

                surname_label = QLabel(self)
                surname_label.setText(user.surname if not None else "")
                self.data_layout.addWidget(surname_label, index, 1)

                email_label = QLabel(self)
                email_label.setText(user.email if not None else "")
                self.data_layout.addWidget(email_label, index, 2)

                phone_label = QLabel(self)
                phone_label.setText(user.phone if not None else "")
                self.data_layout.addWidget(phone_label, index, 3)

                role_combo = QComboBox(self)
                role_combo.addItems([role for role in Role.__members__])
                self.data_layout.addWidget(role_combo, index, 4)
                role_combo.setCurrentText(user.role)
                role_combo.currentTextChanged.connect(lambda text, idx = user.id: self.change_role(idx, role_combo))



                counter += 1

        self.data_layout.setRowStretch(counter+1, 1)
    def change_role(self, idx: int, role_combo: QComboBox):
        with self.database.session() as session:
            user = session.get(Users, idx)
            new_role = role_combo.currentText()
            user.role = Role[new_role]
            session.commit()

