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
    def __init__(self, database, project_id, user):
        super().__init__()
        self.database = database
        self.project_id = project_id
        self.user = user

        self.layout = QGridLayout()
        self.setLayout(self.layout)




        self.name_label = QLabel(self)
        self.name_label.setText(self.user.name)
        self.layout.addWidget(self.name_label, 0, 0)