from helper import (
    hash_password,
    validate_password,
    email_validation,
    save_login,
    delete_login,
)
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QGridLayout,
    QPushButton,
    QDialog,
    QLabel,
    QLineEdit,
    QTextEdit,
    QMessageBox,
    QCheckBox,
    QScrollArea,
)
from windows.sign_in_page import SignIn
from datetime import datetime
from models import Projects, ProjectDetails, Users, Role, Logs, Log
from PySide6.QtGui import Qt
from functools import partial

class LoginWindow(QDialog):
    def __init__(self, database, token):
        super().__init__()

        self.database = database

        self.token = token

        self.user_id = None

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.setWindowTitle("Login")

        self.email_label = QLabel(self)
        self.email_label.setText("Email Address")
        self.layout.addWidget(self.email_label, 0, 0)

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email Address")
        self.layout.addWidget(self.email_input, 0, 1)

        self.password_label = QLabel(self)
        self.password_label.setText("Password")
        self.layout.addWidget(self.password_label, 1, 0)
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumWidth(200)
        self.layout.addWidget(self.password_input, 1, 1)

        self.password_visibility_checkbox = QCheckBox(self)
        self.password_visibility_checkbox.setText("show password")
        self.password_visibility_checkbox.clicked.connect(self.checkbox_function)
        self.layout.addWidget(self.password_visibility_checkbox, 1, 2)

        self.login_button = QPushButton(self)
        self.login_button.setText("LOGIN")
        self.layout.addWidget(self.login_button, 2, 1)
        self.login_button.clicked.connect(self.login_button_function)

        self.cancel_button = QPushButton(self)
        self.cancel_button.setText("CANCEL")
        self.layout.addWidget(self.cancel_button, 2, 2)
        self.cancel_button.clicked.connect(self.cancel_button_function)

        self.sign_in_label = QLabel(self)
        self.sign_in_label.setText('<a href="#">Sign In</a>')
        self.layout.addWidget(self.sign_in_label, 3, 1)
        self.sign_in_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.sign_in_label.linkActivated.connect(self.sign_in_link)

        self.remember_me_checkbox = QCheckBox(self)
        self.remember_me_checkbox.setText("Remember Me")
        self.layout.addWidget(self.remember_me_checkbox, 3, 0)
        if self.token is not None:
            self.remember_me_checkbox.setChecked(True)
        self.remember_me_checkbox.clicked.connect(self.remember_checkbox_function)

        # check if exist user with id like token number. If yes fulfill email input with user email
        if self.token is not None:
            with self.database.session() as session:
                user = session.get(Users, self.token)
                if user:
                    self.email_input.setText(user.email)

    def remember_checkbox_function(self):
        if self.remember_me_checkbox.isChecked():
            return True
        else:
            return False

    def login_button_function(self):

        email = self.email_input.text()
        password = self.password_input.text()

        if not (email and password):
            warning = QMessageBox()
            warning.setText("Please enter your email and password")
            warning.exec()
            return

        with self.database.session() as session:
            row = session.query(Users).filter(Users.email == email).first()
            if row is not None:
                if hash_password(password) == row.password:
                    log = Logs(activity=Log.LOGIN.value, user_id=row.id)
                    session.add(log)
                    session.commit()
                else:
                    wrong_password_message = QMessageBox()
                    wrong_password_message.setText("Wrong password. Please try again")
                    wrong_password_message.exec()
                    return
                # Crete txt file with logged user.id if checkbox remember_me is checked
                if self.remember_me_checkbox.isChecked():
                    save_login(user_id=row.id)
                else:
                    try:
                        delete_login()
                    except FileNotFoundError:
                        pass
                message = QMessageBox()
                message.setText("You have logged in successfully")
                message.exec()
                self.user_id = row.id
                self.accept()

            else:
                message = QMessageBox()
                message.setText("There is no account with that email address")
                message.exec()

    def sign_in_link(self):
        sign_in = SignIn(self.database)
        self.setEnabled(False)
        sign_in.exec()
        self.setEnabled(True)

    def checkbox_function(self):
        if self.password_visibility_checkbox.isChecked():
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

    def cancel_button_function(self):
        self.reject()