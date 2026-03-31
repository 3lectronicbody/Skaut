from helper import (
    hash_password,
    validate_password,
    email_validation,
    load_config,
    save_config
)
from PySide6.QtWidgets import (
    QGridLayout,
    QPushButton,
    QDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QCheckBox,

)
from models import Users, Role
from PySide6.QtCore import Signal




class SignIn(QDialog):
    sign_in_signal = Signal()
    def __init__(self, database, controller):
        super().__init__()
        self.database = database
        self.controller = controller
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.label = QLabel(self)
        self.label.setText("Email Address:")
        self.layout.addWidget(self.label, 0, 0)
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email Address")
        self.layout.addWidget(self.email_input, 0, 1)

        self.password_label = QLabel(self)
        self.password_label.setText("Password:")
        self.layout.addWidget(self.password_label, 1, 0)
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password_input, 1, 1)

        self.password_visibility_checkbox = QCheckBox(self)
        self.password_visibility_checkbox.setChecked(False)
        self.password_visibility_checkbox.setText("   Show\nPassword")
        self.layout.addWidget(self.password_visibility_checkbox, 1, 2)
        self.password_visibility_checkbox.clicked.connect(self.click_checkbox)

        self.rep_password_label = QLabel(self)
        self.rep_password_label.setText("Repeat password:")
        self.layout.addWidget(self.rep_password_label, 2, 0)
        self.rep_password_input = QLineEdit(self)
        self.rep_password_input.setPlaceholderText("Password")
        self.rep_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.rep_password_input, 2, 1)

        self.create_account_button = QPushButton(self)
        self.create_account_button.setText("Create Account")
        self.layout.addWidget(self.create_account_button, 3, 0)
        self.create_account_button.clicked.connect(self.create_account_function)

        self.cancel_button = QPushButton(self)
        self.cancel_button.setText("Cancel")
        self.layout.addWidget(self.cancel_button, 3, 1)
        self.cancel_button.clicked.connect(self.cancel_button_function)

    def cancel_button_function(self):
        self.deleteLater()
        self.controller.show_login_window()

    def click_checkbox(self):
        if self.password_visibility_checkbox.isChecked():
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

    def create_account_function(self):
        email = self.email_input.text()
        password = self.password_input.text()
        rep_password = self.rep_password_input.text()
        # check email validation
        em_valid, em_message = email_validation(email, self.database)
        if not em_valid:
            QMessageBox(text=f"{em_message}").exec()
            return

        # Check if password and repeat password are the same
        if password != rep_password:
            QMessageBox(text="Passwords do not match!").exec()
            return
        # Validate password for characters and length
        pas_valid, pas_message = validate_password(password)
        if pas_valid:
            hashed_password = hash_password(password)
            with self.database.session() as session:
                new_user = Users(
                    email=email, password=hashed_password, role=Role.USER.value
                )
                session.add(new_user)
                session.commit()
                session.close()
            QMessageBox(text="Your Account has been created !!!").exec()

            data = load_config()
            data["remembered_email"] = email
            data["remember_checkbox"] = True
            save_config(data)
            self.sign_in_signal.emit()
            self.accept()
        else:
            QMessageBox(text=f"{pas_message}").exec()
