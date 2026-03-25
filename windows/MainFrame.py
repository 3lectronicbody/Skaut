from PySide6.QtCore import Signal
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QMessageBox, QMenuBar
from models import Users
from windows.main_menu_page import MenuPage
from windows.new_project_page import NewProjectWindow
from windows.user_page import UserWindow
from windows.all_projects_page import ProjectsWindow
from windows.admin_page import AdminWindow
from windows.single_project_page import SingleProject

class MainStack(QMainWindow):
    # Signal to notify controller that user clicked logout
    logout_signal = Signal()

    def __init__(self, database, user_id, project_id=None):
        super().__init__()
        self.database = database
        self.user_id = user_id
        self.project_id = project_id



        # Load user object from DB
        with self.database.session() as session:
            self.user = session.get(Users, self.user_id)

        self.move(500, 250)

        # Central stacked widget for pages
        self.central_widget = QStackedWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create pages
        self.main_menu = MenuPage(self.database, self.user, self)
        self.new_project_page = NewProjectWindow(self.database, self.user, self)
        self.user_page = UserWindow(self.database, self.user, self)
        self.all_projects_page = ProjectsWindow(self.database, self.user, self)
        self.admin_page = AdminWindow(self.database, self.user, self)
        self.single_project_page = SingleProject(self.database, self.user, self.project_id,self)

        # Add menu to Main Frame
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)
        # Add options to menubar
        self.file_menu = self.menu_bar.addMenu("File")
        self.file_menu.addAction("Main Menu", self.show_main_page)
        self.file_menu.addAction("New Project", self.show_new_project_page)
        self.file_menu.addAction("My Account", self.show_user_page)
        self.file_menu.addAction("All Projects", self.show_all_projects_page)

        # Add pages to stack
        self.central_widget.addWidget(self.main_menu)
        self.central_widget.addWidget(self.new_project_page)
        self.central_widget.addWidget(self.user_page)
        self.central_widget.addWidget(self.all_projects_page)
        self.central_widget.addWidget(self.admin_page)
        self.central_widget.addWidget(self.single_project_page)

        self.central_widget.setCurrentWidget(self.main_menu)

    # --- Close Event ---
    def closeEvent(self, event: QCloseEvent):
        # If user requested logout, skip confirmation. Early return interrupt rest of close
        # event procedure which include
        if self._logging_out:
            event.accept()
            return

        # Otherwise, ask for confirmation
        message = QMessageBox(self)
        message.setText("Are you sure you want to leave the application?")
        message.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        result = message.exec()
        if result == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

    # --- Navigation Methods ---
    def show_main_page(self):
        self.central_widget.setCurrentWidget(self.main_menu)

    def show_new_project_page(self):
        self.central_widget.setCurrentWidget(self.new_project_page)

    def show_user_page(self):
        self.central_widget.setCurrentWidget(self.user_page)

    def show_all_projects_page(self):
        self.all_projects_page.refresh_layout()
        self.central_widget.setCurrentWidget(self.all_projects_page)

    def show_admin_page(self):
        self.central_widget.setCurrentWidget(self.admin_page)

    def show_single_project(self, project_id):
        self.single_project_page.load_project(project_id)
        self.central_widget.setCurrentWidget(self.single_project_page)





    # --- Logout Method ---
    def request_logout(self):
        """Call this method when user clicks Logout button"""
        self._logging_out = True  # Flag to skip confirmation
        self.logout_signal.emit()
