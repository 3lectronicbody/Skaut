
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

from windows.menu_page import MenuPage
from windows.new_project_page import NewProjectWindow


class MainStack(QMainWindow):
    def __init__(self, database, user_id):
        super().__init__()

        self.database = database
        self.user_id = user_id
        # Get user based on id and save it in self.user variable for later use in main window
        with self.database.session() as session:
            self.user = session.get(Users, self.user_id)


        self.move(500, 250)

        self.central_widget = QStackedWidget(self)
        self.setCentralWidget(self.central_widget)

        self.main_menu = MenuPage(self.database, self.user, self)
        self.new_project_page = NewProjectWindow(self.database, self.user, self)


        self.central_widget.addWidget(self.main_menu)
        self.central_widget.addWidget(self.new_project_page)

        self.central_widget.setCurrentWidget(self.main_menu)

    def show_main_page(self):
        self.central_widget.setCurrentWidget(self.main_menu)

    def show_new_project_page(self):
        self.central_widget.setCurrentWidget(self.new_project_page)









