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

class SingleProject(QWidget):
    def __init__(self, database, user, project_id, stack):
        super().__init__()
        self.database = database
        self.user = user
        self.project_id = project_id
        self.stack = stack

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.name_label = QLabel(self)
        self.name_label.setText(self.user.name)
        self.layout.addWidget(self.name_label, 0, 0)

        self.project_name_label = QLabel(self)
        self.project_name_label.setText("loaded content")
        self.layout.addWidget(self.project_name_label, 0, 1)

        self.back_button = QPushButton(self)
        self.back_button.setText("Back")
        self.layout.addWidget(self.back_button, 0, 2)
        self.back_button.clicked.connect(self.stack.show_all_projects_page)

    def load_project(self, project_id):
        with self.database.session() as session:
            loaded_project = session.get(Projects, project_id)
        if loaded_project:
            self.project_name_label.setText(loaded_project.name)







