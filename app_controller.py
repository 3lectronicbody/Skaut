from PySide6.QtCore import QObject
from windows.login_window import LoginWindow
from windows.sign_in_page import SignIn
from windows.MainFrame import MainStack
from helper import load_login

class AppController(QObject):
    def __init__(self, database):
        super().__init__()
        self.database = database
        self.token = load_login()
        self.user_id = None


        self.login_window = LoginWindow(self.database, self.token)
        self.login_window.login_signal.connect(self.logged_in)

        self.main_frame = None

        self.sign_in_window = SignIn(self.database)


    def logged_in(self):
        self.main_frame = MainStack(self.database, self.user_id)
        self.main_frame.show()

