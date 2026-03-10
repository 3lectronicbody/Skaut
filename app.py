from PySide6.QtWidgets import QApplication, QDialog
import qdarkstyle
import sys
from database import Database
from helper import load_login
from main import MainWindow, LoginWindow
from models import Logs, Log

def main_app():
    # APPLICATION FLOW:

    # 1. Start application
    app = QApplication(sys.argv)
    # 2. Set dark style
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    # 3. Create database object
    database_object = Database()
    # 4. Try to load token from txt file. If exists, create login window with token, if not create login window without token
    try:
        token = load_login()
    except FileNotFoundError:
        token = None
    # 5. Create login window
    login = LoginWindow(database_object, token)
    # 6. If user logged in successfully, open main window, if not exit application
    if login.exec() == QDialog.DialogCode.Accepted:
        main_window = MainWindow(database_object, login.user_id) # login.user_id - id of user who logged in
        main_window.show()
        # When user closes main window, log out activity in database and exit application
        with database_object.session() as session:
            log = Logs(activity=Log.LOGOUT.value, user_id=login.user_id)
            session.add(log)
            session.commit()
        sys.exit(app.exec())
    else:
        sys.exit()

if __name__ == "__main__":
    main_app()


