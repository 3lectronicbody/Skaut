from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel
from models import Users

from database import Database


class EmployeesWindow(QWidget):
    def __init__(self, database: Database):
        super().__init__()

        self.database = database

        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)

        self.data_layout = QGridLayout()
        self.main_layout.addLayout(self.data_layout, 0, 0)

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

                counter += 1

        self.data_layout.setRowStretch(counter+1, 1)

