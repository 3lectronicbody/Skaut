import hashlib
import tempfile

from email_validator import validate_email, EmailNotValidError
from models import Users
from sqlalchemy import select
import os
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton, QGridLayout


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def validate_password(password: str) -> tuple[bool, str]:
    # Password must be at least 8 characters
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    # Password must contain at least 1 number
    # Password must contain at least one special character
    digit = False
    special = False
    for c in password:
        if c.isdigit():
            digit = True
        elif c.isalnum():
            special = True
    if not digit:
        return False, "Password must contain at least one digit"
    if not special:
        return False, "Password must contain at least one special character"
    return True, "Password is valid"

def email_validation(email: str, database) -> tuple[bool, str]:
    # 1 - email validation with module email_validator
    try:
        validate_email(email)
    except EmailNotValidError:
        return False, "Email is not valid"

    # 2 - check if email exists in database. If so there already exists account.
    with database.session() as session:
        statement = select(Users.email).where(Users.email == email)
        existing = session.scalars(statement).first()
        if existing:
            return False, "Account with this email already exists"
    return True, "Password is valid"

def save_login(user_id: str):
    with open("token.txt", "w") as token:
        token.write(str(user_id))
    return int(user_id)

def load_login():
    with open("token.txt", "r") as token:
        token = token.read()
        return token


def delete_login():
    try:
        os.remove("token.txt")
    except FileNotFoundError:
        pass
def reset_password(user_email):
    pass

def ok_message(message: str):
    message_window = QDialog()
    layout = QVBoxLayout()
    message_window.setLayout(layout)
    message_label = QLabel(message)

    layout.addWidget(message_label)

    ok_button = QPushButton("Ok")
    layout.addWidget(ok_button)
    ok_button.clicked.connect(message_window.accept)


    message_window.exec()

def confirmation_message(message: str):
    confirmation = QDialog()
    layout = QGridLayout()

    confirmation.setLayout(layout)

    message_label = QLabel()
    message_label.setText(message)
    layout.addWidget(message_label, 0, 0, 1, 2)

    back_button = QPushButton()
    back_button.setText("BACK")
    layout.addWidget(back_button, 1, 0)

    confirm_button = QPushButton()
    confirm_button.setText("CONFIRM")
    confirm_button.setStyleSheet(back_button.styleSheet())
    confirm_button.setStyleSheet("color: green;")
    layout.addWidget(confirm_button, 1, 1)



    confirm_button.clicked.connect(confirmation.accept)
    back_button.clicked.connect(confirmation.reject)

    return confirmation.exec()




