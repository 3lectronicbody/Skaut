from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QPushButton,
    QLabel,
    QLineEdit,
)
from models import  Users


class UserWindow(QWidget):
    def __init__(self, database,user, parent):
        super().__init__()
        self.database = database
        self.user = user
        self.parent = parent


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
        self.cancel_button.setText("CANCEL")
        self.layout.addWidget(self.cancel_button, 1, 0)
        self.cancel_button.clicked.connect(lambda: self.parent.show_main_page())



        # Widgets
    def refresh_layout(self):
        layout = self.ref_layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
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
        self.ref_layout.addWidget(edit_name_button, 0, 2)
        def edit_button_clicked():
            edit_name_button.setDisabled(True)
            surname_input.setEnabled(True)
            save_name_button.setEnabled(True)
        edit_name_button.clicked.connect(edit_button_clicked)


        save_name_button = QPushButton(self)
        save_name_button.setText("Save...")
        save_name_button.setDisabled(True)
        self.ref_layout.addWidget(save_name_button, 0, 3)
        def save_button_clicked():
            with self.database.session() as session:
                if not surname_input.text():
                    edit_name_button.setEnabled(True)
                    return
                user = session.get(Users, self.user.id)
                if user:
                    user.name = surname_input.text()
                    session.commit()
                    surname_input.setText(user.name)
                    surname_input.setEnabled(False)
                    save_name_button.setDisabled(True)
                    edit_name_button.setEnabled(True)
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
        self.ref_layout.addWidget(edit_surname_button, 1, 2)
        def edit_surname_button_clicked():
            edit_surname_button.setDisabled(True)
            surname_input.setEnabled(True)
            save_surname_button.setEnabled(True)
        edit_surname_button.clicked.connect(edit_surname_button_clicked)


        save_surname_button = QPushButton(self)
        save_surname_button.setText("Save...")
        save_surname_button.setDisabled(True)
        self.ref_layout.addWidget(save_surname_button, 1, 3)

        def save_surname_button_clicked():
            with self.database.session() as session:
                if not surname_input.text():
                    edit_surname_button.setEnabled(True)
                    return
                user = session.get(Users, self.user.id)
                if user:
                    user.surname = surname_input.text()
                    session.commit()
                    surname_input.setText(user.surname)
                    surname_input.setEnabled(False)
                    save_surname_button.setDisabled(True)
                    edit_surname_button.setEnabled(True)

        save_surname_button.clicked.connect(save_surname_button_clicked)

        rows = self.ref_layout.rowCount()
        self.ref_layout.setRowStretch(rows+1, 1)
