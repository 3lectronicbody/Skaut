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
    QScrollArea,
)
from datetime import datetime
from models import Projects, ProjectDetails, Users, Role, Logs, Log
from PySide6.QtGui import Qt
from functools import partial



class NewProjectWindow(QDialog):
    def __init__(self, database, user, stack):
        super().__init__()
        self.database = database
        self.user = user
        self.stack = stack

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.name_label = QLabel(self)
        self.name_label.setText("Name")
        self.layout.addWidget(self.name_label, 0, 0)
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Name")
        self.layout.addWidget(self.name_input, 0, 1)

        self.description_label = QLabel(self)
        self.description_label.setText("Description")
        self.layout.addWidget(self.description_label, 1, 0)
        self.description_input = QTextEdit(self)
        self.description_input.setPlaceholderText("Description")
        self.layout.addWidget(self.description_input, 1, 1)

        self.save_button = QPushButton(self)
        self.save_button.setText("CREATE")
        self.layout.addWidget(self.save_button, 3, 1)
        self.save_button.clicked.connect(self.save_project)

        self.cancel_button = QPushButton(self)
        self.cancel_button.setText("CANCEL")
        self.layout.addWidget(self.cancel_button, 3, 0)
        self.cancel_button.clicked.connect(self.stack.show_main_page)

    def save_project(self):
        name = self.name_input.text()
        description = self.description_input.toPlainText()
        beginning_date = datetime.now()
        project_owner = self.user.email
        if name and description:
            message = QMessageBox()
            message.setText("Are You sure you want to create this project?")
            message.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if message.exec() == QMessageBox.StandardButton.Yes:
                with self.database.session() as session:
                    project = Projects(
                        name=name,
                        description=description,
                        project_owner=project_owner,
                        beginning=beginning_date,
                    )
                    session.add(project)
                    session.flush()

                    # Log activity in database
                    log = Logs(
                        activity=Log.CREATE_PROJECT.value,
                        user_id=self.user.id,
                        project_id=project.id,
                    )
                    session.add(log)
                    session.commit()
                from helper import ok_message
                ok_message("Project has been created successfully")
                self.name_input.setText("")
                self.description_input.setText("")
                self.stack.show_main_page()
        else:
            warning_message = QMessageBox()
            warning_message.setText("Please enter name of project and description")
            warning_message.exec()

