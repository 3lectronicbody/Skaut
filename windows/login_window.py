
from PySide6.QtCore import Signal, QTimer
from PySide6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QCheckBox, QGridLayout, QMessageBox
)
from PySide6.QtGui import Qt
from helper import hash_password, save_login, delete_login, ok_message
from models import Users, Logs, Log
from config import CONFIG_FILE
import json


class LoginWindow(QDialog):
    # Signals to communicate with controller
    login_signal = Signal(int)       # Emits user_id on successful login
    signup_signal = Signal()         # Emits when user clicks "Sign In / Sign Up"

    def __init__(self, database,token=None, controller=None):
        super().__init__()
        self.database = database
        self.user_id = None
        self.controller = controller
        self.config_file = CONFIG_FILE

        self.caps_timer = QTimer(self)
        self.caps_timer.timeout.connect(self.caps_state)
        self.caps_timer.start(200)



        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.setWindowTitle("Login")

        # --- UI Elements ---
        self.email_label = QLabel("Email Address")
        self.layout.addWidget(self.email_label, 0, 0)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email Address")
        self.email_input.setMinimumWidth(300)
        self.layout.addWidget(self.email_input, 0, 1)

        self.password_label = QLabel("Password")
        self.layout.addWidget(self.password_label, 1, 0)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.installEventFilter(self)
        # Connect capslock check function to default text change signal in password input
        self.password_input.textChanged.connect(self.caps_state)
        self.layout.addWidget(self.password_input, 1, 1)

        self.password_checkbox = QCheckBox("Show Password")
        self.password_checkbox.clicked.connect(self.toggle_password_visibility)
        self.layout.addWidget(self.password_checkbox, 1, 2)

        self.login_button = QPushButton("LOGIN")
        self.login_button.clicked.connect(self.login_button_function)
        self.login_button.setMaximumWidth(100)
        self.layout.addWidget(self.login_button, 2, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        self.cancel_button = QPushButton("CANCEL")
        self.cancel_button.clicked.connect(self.reject)
        self.layout.addWidget(self.cancel_button, 2, 2)

        self.sign_in_label = QLabel('<a href="#">Sign In</a>')
        self.sign_in_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.sign_in_label, 3, 1)
        self.sign_in_label.linkActivated.connect(self.sign_in_link)

        self.remember_checkbox = QCheckBox("Remember Me")
        self.layout.addWidget(self.remember_checkbox, 3, 0)


        self.caps_label = QLabel("")
        self.layout.addWidget(self.caps_label, 4, 0)

        self.caps_state()

        # Pre-fill email if token exists
        if self.token:
            with self.database.session() as session:
                user = session.get(Users, self.token)
                if user:
                    self.email_input.setText(user.email)

    # --- Button Methods ---
    def toggle_password_visibility(self):
        if self.password_checkbox.isChecked():
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

    def login_button_function(self):
        email = self.email_input.text()
        password = self.password_input.text()
        if not (email and password):
            QMessageBox.warning(self, "Warning", "Please enter your email and password")
            return

        with self.database.session() as session:
            user = session.query(Users).filter(Users.email == email).first()
            if not user:
                QMessageBox.warning(self, "Warning", "No account found with that email")
                return

            if hash_password(password) != user.password:
                QMessageBox.warning(self, "Warning", "Wrong password. Try again")
                return

            # Successful login
            log = Logs(activity=Log.LOGIN.value, user_id=user.id)
            session.add(log)
            session.commit()

            if self.remember_checkbox.isChecked():
                save_login(user.id)
            else:
                try:
                    delete_login()
                except FileNotFoundError:
                    pass

            ok_message("You have successfully logged in")
            self.user_id = user.id
            self.login_signal.emit(user.id)
            self.accept()

    def sign_in_link(self):
        # Notify controller to open SignIn window
        self.signup_signal.emit()
    def caps_state(self):
        caps_on = bool(Quartz.CGEventSourceFlagsState(
            Quartz.kCGEventSourceStateHIDSystemState
        ) & Quartz.kCGEventFlagMaskAlphaShift)
        if caps_on:
            self.caps_label.setText("CAPS_ON")
        else:
            self.caps_label.setText("")







