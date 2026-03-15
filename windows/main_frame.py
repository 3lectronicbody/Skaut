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
from datetime import datetime
from models import Projects, ProjectDetails, Users, Role, Logs, Log
from PySide6.QtGui import Qt
from functools import partial

class MainWindow(QMainWindow):
    def __init__(self, database, user_id):
        super().__init__()
        self.database = database

        # Logged User form Login window
        self.user_id = user_id
        # Get iser based on id and save it in self.user variable for later use in main window
        with self.database.session() as session:
            self.user = session.get(Users, self.user_id)

        self.new_project_window = None
        self.all_projects_window = None
        self.user_window = None

        self.move(500, 250)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle("Main Window")
        self.layout = QGridLayout()
        self.central_widget.setLayout(self.layout)

        # WIDGETS
        # Welcome labe
        self.welcome_label = QLabel(self)
        self.welcome_label.setText(f"Welcome to Skaut {self.user.email}")
        self.layout.addWidget(self.welcome_label, 0, 0)
        # Create New Project Button
        self.create_button = QPushButton(self)
        self.create_button.setText("CREATE NEW PROJECT")
        self.layout.addWidget(self.create_button, 1, 0)
        self.create_button.clicked.connect(self.create_project_button)

        # Projects Button
        self.all_projects_button = QPushButton(self)
        self.all_projects_button.setText("PROJECTS")
        self.layout.addWidget(self.all_projects_button, 2, 0)
        self.all_projects_button.clicked.connect(self.all_projects_button_function)

        # User Button
        self.user_button = QPushButton(self)
        self.user_button.setText("USER DASHBOARD")
        self.layout.addWidget(self.user_button, 3, 0)
        self.user_button.clicked.connect(self.user_window_button_function)

        row_count = self.layout.rowCount()
        self.layout.setRowStretch(row_count, 1)

    def user_window_button_function(self):
        self.user_window = UserWindow(self.database, self, self.user)
        self.user_window.show()
        self.hide()

    def create_project_button(self):
        self.new_project_window = NewProjectWindow(self)
        self.hide()
        self.new_project_window.exec()
        self.show()

    def all_projects_button_function(self):
        self.all_projects_window = ProjectsWindow(self.database, self.user)
        self.hide()
        self.all_projects_window.exec()
        self.show()