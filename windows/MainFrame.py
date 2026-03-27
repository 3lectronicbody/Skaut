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
from windows.employees_page import EmployeesWindow

class MainStack(QMainWindow):
    # Signal to notify controller that user clicked logout
    logout_signal = Signal()

    def __init__(self, database, user_id, controller, project_id=None):
        super().__init__()
        self.database = database
        self.user_id = user_id
        self.controller = controller
        self.project_id = project_id
        self._logging_out = False


        self.resize(500,500)
        self.setWindowTitle("Skaut Projects")



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
        self.employees_page = EmployeesWindow(self.database, self)

        # Create Menubar
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)
        # Add options to Menubar
        self.file_menu = self.menu_bar.addMenu("File..")
        self.file_menu.addAction("Logout", self.file_menu_logout_action)
        self.file_menu.addAction("Home Page...", self.show_main_page)

        self.about_menu = self.menu_bar.addMenu("About")
        self.about_menu.addAction("About...", self.about_menu_dialog)

        # Add pages to stack
        self.central_widget.addWidget(self.main_menu)
        self.central_widget.addWidget(self.new_project_page)
        self.central_widget.addWidget(self.user_page)
        self.central_widget.addWidget(self.all_projects_page)
        self.central_widget.addWidget(self.admin_page)
        self.central_widget.addWidget(self.single_project_page)
        self.central_widget.addWidget(self.employees_page)

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

    def show_employees_page(self):
        self.central_widget.setCurrentWidget(self.employees_page)


    # --- Logout Method ---
    def request_logout(self):
        """Call this method when user clicks Logout button"""
        self._logging_out = True  # Flag to skip confirmation
        self.logout_signal.emit()
    def about_menu_dialog(self):
        about_dialog = QMessageBox(self)
        about_dialog.setWindowTitle("About")
        from config import VERSION
        about_dialog.setText(f"Application Version: {VERSION}\nLogged User: {self.user.email}")
        about_dialog.exec()
    def file_menu_logout_action(self):
        self.request_logout()
