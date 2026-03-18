from PySide6.QtWidgets import QApplication, QDialog, QMessageBox
import qdarkstyle
import sys
from database import Database
from helper import load_login
from windows.login_window import LoginWindow
from windows.MainFrame import MainStack
from app_controller import AppController
from models import Logs, Log


def main_app():
    # APPLICATION FLOW:
    app = QApplication(sys.argv)
    database = Database()
    controller = AppController(database)
    controller.start()
    app.exec()


if __name__ == "__main__":
    main_app()
