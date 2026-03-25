from PySide6.QtCore import QObject
from windows.login_window import LoginWindow
from windows.sign_in_page import SignIn
from windows.MainFrame import MainStack
from helper import load_login, delete_login

class AppController(QObject):
    def __init__(self, database):
        super().__init__()
        self.database = database
        try:
            self.token = load_login()
        except FileNotFoundError:
            self.token = None
        self.user_id = None

        # References to windows
        self.login_window = None
        self.sign_in_window = None
        self.main_frame = None

    # Start the app
    def start(self):
        # self.show_login_window()
        self.show_main_frame(user_id=1)
    def show_login_window(self):
        self.login_window = LoginWindow(self.database, self.token, controller=self)
        # Connect signals
        self.login_window.login_signal.connect(self.show_main_frame)
        self.login_window.signup_signal.connect(self.show_sign_in_window)  # new
        self.login_window.show()

        if self.main_frame:
            self.main_frame.hide()
        if self.sign_in_window:
            self.sign_in_window.hide()

    def show_sign_in_window(self):
        self.sign_in_window = SignIn(self.database, controller=self)
        self.sign_in_window.sign_in_signal.connect(self.show_login_window)
        self.sign_in_window.show()
        if self.login_window:
            self.login_window.hide()
        if self.main_frame:
            self.main_frame.hide()

    def show_main_frame(self, user_id):
        self.user_id = user_id
        if self.main_frame:
            self.main_frame.close()
            self.main_frame.deleteLater()
            self.main_frame = None

        if self.main_frame is None:
            self.main_frame = MainStack(self.database, self.user_id)
            # Connect main window logout signal to controller
            self.main_frame.logout_signal.connect(self.handle_logout)
        self.main_frame.show()
        if self.login_window:
            self.login_window.hide()
        if self.sign_in_window:
            self.sign_in_window.hide()

    def handle_logout(self):
        try:
            delete_login()
        except FileNotFoundError:
            pass
        if self.main_frame:
            self.main_frame.close()
            self.main_frame.deleteLater()
            self.main_frame = None
        self.show_login_window()