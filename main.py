import sys
# import qdarkstyle
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QDialog, QLabel, QLineEdit, \
    QTextEdit, QMessageBox
from datetime import datetime
from database import Database
from models import Projects, ProjectDetails


class MainWindow(QMainWindow):
    def __init__(self,database):
        super().__init__()
        self.database = database

        self.new_project_window = None
        self.all_projects_window = None


        self.move(500, 250)


        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle("Main Window")
        self.layout = QGridLayout()
        self.central_widget.setLayout(self.layout)

        # WIDGETS

        # Create New Project Button
        self.create_button = QPushButton(self)
        self.create_button.setText("CREATE NEW PROJECT")
        self.layout.addWidget(self.create_button, 0, 0)
        self.create_button.clicked.connect(self.create_project_button)

        # Projects Button
        self.all_projects_button = QPushButton(self)
        self.all_projects_button.setText("PROJECTS")
        self.layout.addWidget(self.all_projects_button, 1, 0)
        self.all_projects_button.clicked.connect(self.all_projects_button_function)



    def create_project_button(self):
        self.new_project_window = NewProjectWindow(self)
        self.hide()
        self.new_project_window.exec()
        self.show()

    def all_projects_button_function(self):
        self.all_projects_window = ProjectsWindow(self.database)
        self.hide()
        self.all_projects_window.exec()
        self.show()

class LoginWindow(QDialog):
    def __init__(self, database):
        super().__init__()

        self.database = database

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.username_label = QLabel(self)
        self.username_label.setText("Username")
        self.layout.addWidget(self.username_label, 0, 0)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        self.layout.addWidget(self.username_input, 0, 1)

        self.password_label = QLabel(self)
        self.password_label.setText("Password")
        self.layout.addWidget(self.password_label, 1, 0)
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.layout.addWidget(self.password_input, 1, 1)

        self.login_button = QPushButton(self)
        self.login_button.setText("LOGIN")
        self.layout.addWidget(self.login_button, 2, 1)
        self.login_button.clicked.connect(self.login_button_function)

        self.cancel_button = QPushButton(self)
        self.cancel_button.setText("CANCEL")
        self.layout.addWidget(self.cancel_button, 2, 2)
        self.cancel_button.clicked.connect(self.cancel_button_function)
    def login_button_function(self):
        self.accept()

    def cancel_button_function(self):
        self.reject()

class NewProjectWindow(QDialog):
    def __init__(self, parent_window):
        super().__init__()
        self.main_window = parent_window
        self.database = parent_window.database


        # Get current main window position
        main_pos = self.main_window.frameGeometry().topLeft()
        # Move dialog to same position
        self.move(main_pos)

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.name_label = QLabel(self)
        self.name_label.setText("Name")
        self.layout.addWidget(self.name_label, 0, 0)
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Name")
        self.layout.addWidget(self.name_input, 0, 1)

        self.owner_label = QLabel(self)
        self.owner_label.setText("Owner")
        self.layout.addWidget(self.owner_label, 1, 0)
        self.owner_input = QLineEdit(self)
        self.owner_input.setPlaceholderText("Owner")
        self.layout.addWidget(self.owner_input, 1, 1)

        self.description_label = QLabel(self)
        self.description_label.setText("Description")
        self.layout.addWidget(self.description_label, 2, 0)
        self.description_input = QTextEdit(self)
        self.description_input.setPlaceholderText("Description")
        self.layout.addWidget(self.description_input, 2, 1)

        self.save_button = QPushButton(self)
        self.save_button.setText("SAVE")
        self.layout.addWidget(self.save_button, 3, 0)
        self.save_button.clicked.connect(self.save_project)

        self.cancel_button = QPushButton(self)
        self.cancel_button.setText("CANCEL")
        self.layout.addWidget(self.cancel_button, 3, 1)
        self.cancel_button.clicked.connect(self.close)

    def save_project(self):
        name = self.name_input.text()
        owner = self.owner_input.text()
        description = self.description_input.toPlainText()
        beginning_date = datetime.now().strftime("%m/%d/%Y")
        session = self.database.session()
        session.add(Projects(name=name,description=description, project_owner=owner, beginning=beginning_date))
        print("Row added to database")
        session.commit()
        session.close()
        self.close()

class ProjectsWindow(QDialog):
    def __init__(self, database):
        super().__init__()

        self.database = database

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.refresh_layout()

    def refresh_layout(self):
        # Clear current layout
        layout = self.layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        # Populate layout from database
        table = self.database.fetch_table("projects")
        counter = 0
        for i, row in enumerate(table):
            name_label = QLabel(self)
            name_label.setText(row["name"])
            self.layout.addWidget(name_label, i, 0)

            description_label = QLabel(self)
            description_label.setText(row["description"])
            self.layout.addWidget(description_label, i, 1)

            edit_button = QPushButton(self)
            edit_button.setText("EDIT")
            self.layout.addWidget(edit_button, i, 2)
            edit_button.clicked.connect(lambda checked, idx=row['id']: self.edit_button_clicked(idx))

            delete_button = QPushButton(self)
            delete_button.setText("DELETE")
            self.layout.addWidget(delete_button, i, 3)
            delete_button.clicked.connect(lambda checked, idx=i: self.delete_button_clicked(idx))

            counter += 1

        self.cancel_button = QPushButton(self)
        self.cancel_button.setText("CANCEL")
        self.layout.addWidget(self.cancel_button, counter + 1, 0)
        self.cancel_button.clicked.connect(self.close)

class SingleProject(QDialog):
    def __init__(self, database, index):
        super().__init__()
        self.database = database
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.index = index

        table = list(self.database.fetch_table("projects"))
        row = table[self.index]

        self.name_label = QLabel(self)
        self.name_label.setText(str(row['name']))
        self.layout.addWidget(self.name_label, 0, 0)


# APPLICATION FLOW

app = QApplication(sys.argv)

database_object = Database()

login = LoginWindow(database_object)

if login.exec() == QDialog.DialogCode.Accepted:
    main_window = MainWindow(database_object)
    main_window.show()
    sys.exit(app.exec())
else:
    sys.exit()




