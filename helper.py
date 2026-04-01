import hashlib
from email_validator import validate_email, EmailNotValidError
from models import Users
from sqlalchemy import select
import os
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton, QGridLayout
import json



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

def load_config(file="config.json"):
    with open(file, "r") as json_file:
        return json.load(json_file)
def save_config(data, file="config.json"):
    with open(file, "w") as json_file:
        json.dump(data, json_file, indent=4)


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

def load_remembered_user(config_file):
    with open(config_file, "r") as file:
        data = json.load(file)
    return data.get("remember_me", default="")









