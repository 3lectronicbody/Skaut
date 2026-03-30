
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QPushButton,
    QLabel,
    QLineEdit, QVBoxLayout,
)
from models import  Users


class UserWindow(QWidget):
    def __init__(self, database,user, stack):
        super().__init__()
        self.database = database
        self.user = user
        self.stack = stack

        self.edit_buttons = []


        self.setWindowTitle("User Window")
        self.layout = QGridLayout()
        self.setLayout(self.layout)


        self.ref_widget = QWidget(self)
        self.layout.addWidget(self.ref_widget, 0, 0)
        self.ref_layout = QGridLayout()
        self.ref_widget.setLayout(self.ref_layout)

        self.refresh_layout()

        # Cancel button
        self.cancel_button = QPushButton(self)
        self.cancel_button.setText("BACK")
        self.layout.addWidget(self.cancel_button, 1, 0)
        self.cancel_button.clicked.connect(self.handle_back_button)
    def handle_back_button(self):
        self.refresh_layout()
        self.stack.show_main_page()



        # Widgets

    def refresh_layout(self):
        layout = self.ref_layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
    # Clear old list of added buttons
        self.edit_buttons.clear()
    # Name
        name_label = QLabel(self)
        name_label.setText("Name")
        self.ref_layout.addWidget(name_label, 0, 0)

        name_input = QLineEdit(self)
        name_input.setPlaceholderText("Name")
        name_input.setText(self.user.name)
        name_input.setEnabled(False)
        self.ref_layout.addWidget(name_input, 0, 1)

        edit_name_button = QPushButton(self)
        edit_name_button.setText("Edit...")
        self.edit_buttons.append(edit_name_button)
        self.ref_layout.addWidget(edit_name_button, 0, 2)
        def edit_button_clicked():
            name_input.setEnabled(True)
            save_name_button.setEnabled(True)
            for button in self.edit_buttons:
                button.setDisabled(True)
            name_input.setFocus()
        edit_name_button.clicked.connect(edit_button_clicked)


        save_name_button = QPushButton(self)
        save_name_button.setText("Save...")
        save_name_button.setDisabled(True)

        self.ref_layout.addWidget(save_name_button, 0, 3)
        def save_button_clicked():
            with self.database.session() as session:
                if not name_input.text():
                    edit_name_button.setEnabled(True)
                    return
                user = session.get(Users, self.user.id)
                if user:
                    user.name = name_input.text()
                    session.commit()
                    name_input.setText(user.name)
                    name_input.setEnabled(False)
                    save_name_button.setDisabled(True)
                    for button in self.edit_buttons:
                        button.setEnabled(True)
                    self.edit_buttons.clear()

        save_name_button.clicked.connect(save_button_clicked)

    # surname
        surname_label = QLabel(self)
        surname_label.setText("Surname")
        self.ref_layout.addWidget(surname_label, 1, 0)

        surname_input = QLineEdit(self)
        surname_input.setPlaceholderText("Surname")
        surname_input.setText(self.user.surname)
        surname_input.setEnabled(False)
        self.ref_layout.addWidget(surname_input, 1, 1)

        edit_surname_button = QPushButton(self)
        edit_surname_button.setText("Edit...")
        self.edit_buttons.append(edit_surname_button)
        self.ref_layout.addWidget(edit_surname_button, 1, 2)
        def edit_surname_button_clicked():
            surname_input.setEnabled(True)
            save_surname_button.setEnabled(True)
            surname_input.setFocus()
            for button in self.edit_buttons:
                button.setDisabled(True)
        edit_surname_button.clicked.connect(edit_surname_button_clicked)


        save_surname_button = QPushButton(self)
        save_surname_button.setText("Save...")
        save_surname_button.setDisabled(True)
        self.ref_layout.addWidget(save_surname_button, 1, 3)

        def save_surname_button_clicked():
            with self.database.session() as session:
                if not surname_input.text():
                    save_surname_button.setDisabled(True)
                    for button in self.edit_buttons:
                        button.setEnabled(True)
                    return
                user = session.get(Users, self.user.id)
                if user:
                    user.surname = surname_input.text()
                    session.commit()
                    surname_input.setText(user.surname)
                    surname_input.setEnabled(False)
                    save_surname_button.setDisabled(True)

            for button in self.edit_buttons:
                button.setEnabled(True)


        save_surname_button.clicked.connect(save_surname_button_clicked)

    # phone number
        tel_label = QLabel(self)
        tel_label.setText("Phone Number")
        self.ref_layout.addWidget(tel_label,2, 0)

        tel_input = QLineEdit(self)
        tel_input.setPlaceholderText("Phone Number")
        tel_input.setText(self.user.phone)
        tel_input.setEnabled(False)
        self.ref_layout.addWidget(tel_input, 2, 1)

        edit_tel_button = QPushButton(self)
        edit_tel_button.setText("Edit...")
        self.ref_layout.addWidget(edit_tel_button, 2, 2)
        self.edit_buttons.append(edit_tel_button)

        def edit_tel_button_clicked():
            tel_input.setEnabled(True)
            save_tel_button.setEnabled(True)
            for button in self.edit_buttons:
                button.setDisabled(True)

        edit_tel_button.clicked.connect(edit_tel_button_clicked)

        save_tel_button = QPushButton(self)
        save_tel_button.setText("Save...")
        save_tel_button.setDisabled(True)
        self.ref_layout.addWidget(save_tel_button, 2, 3)

        def save_tel_button_clicked():
            with self.database.session() as session:
                if not tel_input.text():
                    save_tel_button.setDisabled(True)
                    for button in self.edit_buttons:
                        button.setEnabled(True)
                    return
                user = session.get(Users, self.user.id)
                if user:
                    user.phone = tel_input.text()
                    session.commit()
                    tel_input.setText(user.phone)
                    tel_input.setEnabled(False)
                    save_tel_button.setDisabled(True)
                    for button in self.edit_buttons:
                        button.setEnabled(True)

        save_tel_button.clicked.connect(save_tel_button_clicked)




        rows = self.ref_layout.rowCount()
        self.ref_layout.setRowStretch(rows+1, 1)
