

from PySide6.QtCore import QObject
from windows.login_window import LoginWindow
from windows.sign_in_page import SignIn
from windows.MainFrame import MainStack
from helper import load_login

class AppController(QObject):
    def __init__(self, database, user_id=None):
        super().__init__()
        self.database = database
        self.token = load_login()


        self.login_window = LoginWindow(self.database)
        self.sign_in_window = SignIn(database)
        self.main_frane = MainStack(database)