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
    QScrollArea, QStackedWidget,
)
from datetime import datetime
from models import Projects, ProjectDetails, Users, Role, Logs, Log
from PySide6.QtGui import Qt
from functools import partial


class MenuPage(QWidget):
    def __init__(self, database, user, parent):
        super().__init__()

        self.database = database
        self.user = user
        self.parent = parent



        self.layout = QGridLayout(self)
        # Welcome labe
        self.welcome_label = QLabel(self)
        self.welcome_label.setText(f"Welcome to Skaut {self.user.email}")
        self.layout.addWidget(self.welcome_label, 0, 0)
        # Create New Project Button
        self.create_button = QPushButton(self)
        self.create_button.setText("CREATE NEW PROJECT")
        self.layout.addWidget(self.create_button, 1, 0)
        self.create_button.clicked.connect(lambda: self.parent.show_new_project_page())


        # Projects Button
        self.all_projects_button = QPushButton(self)
        self.all_projects_button.setText("PROJECTS")
        self.layout.addWidget(self.all_projects_button, 2, 0)


        # User Button
        self.user_button = QPushButton(self)
        self.user_button.setText("USER DASHBOARD")
        self.layout.addWidget(self.user_button, 3, 0)

        row_count = self.layout.rowCount()
        self.layout.setRowStretch(row_count, 1)