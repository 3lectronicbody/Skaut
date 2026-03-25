from PySide6.QtWidgets import QApplication
import qdarkstyle
import sys
from database import Database

from app_controller import AppController



def main_app():
    # APPLICATION FLOW:
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    database = Database()
    controller = AppController(database)
    controller.start()
    app.exec()


if __name__ == "__main__":
    main_app()
