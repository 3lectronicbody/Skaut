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


class LoginWindow(QDialog):
    def __init__(self, database, token):
        super().__init__()

        self.database = database

        self.token = token

        self.user_id = None

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.setWindowTitle("Login")

        self.email_label = QLabel(self)
        self.email_label.setText("Email Address")
        self.layout.addWidget(self.email_label, 0, 0)

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email Address")
        self.layout.addWidget(self.email_input, 0, 1)

        self.password_label = QLabel(self)
        self.password_label.setText("Password")
        self.layout.addWidget(self.password_label, 1, 0)
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumWidth(200)
        self.layout.addWidget(self.password_input, 1, 1)

        self.password_visibility_checkbox = QCheckBox(self)
        self.password_visibility_checkbox.setText("show password")
        self.password_visibility_checkbox.clicked.connect(self.checkbox_function)
        self.layout.addWidget(self.password_visibility_checkbox, 1, 2)

        self.login_button = QPushButton(self)
        self.login_button.setText("LOGIN")
        self.layout.addWidget(self.login_button, 2, 1)
        self.login_button.clicked.connect(self.login_button_function)

        self.cancel_button = QPushButton(self)
        self.cancel_button.setText("CANCEL")
        self.layout.addWidget(self.cancel_button, 2, 2)
        self.cancel_button.clicked.connect(self.cancel_button_function)

        self.sign_in_label = QLabel(self)
        self.sign_in_label.setText('<a href="#">Sign In</a>')
        self.layout.addWidget(self.sign_in_label, 3, 1)
        self.sign_in_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.sign_in_label.linkActivated.connect(self.sign_in_link)

        self.remember_me_checkbox = QCheckBox(self)
        self.remember_me_checkbox.setText("Remember Me")
        self.layout.addWidget(self.remember_me_checkbox, 3, 0)
        if self.token is not None:
            self.remember_me_checkbox.setChecked(True)
        self.remember_me_checkbox.clicked.connect(self.remember_checkbox_function)

        # check if exist user with id like token number. If yes fulfill email input with user email
        if self.token is not None:
            with self.database.session() as session:
                user = session.get(Users, self.token)
                if user:
                    self.email_input.setText(user.email)

    def remember_checkbox_function(self):
        if self.remember_me_checkbox.isChecked():
            return True
        else:
            return False

    def login_button_function(self):

        email = self.email_input.text()
        password = self.password_input.text()

        if not (email and password):
            warning = QMessageBox()
            warning.setText("Please enter your email and password")
            warning.exec()
            return

        with self.database.session() as session:
            row = session.query(Users).filter(Users.email == email).first()
            if row is not None:
                if hash_password(password) == row.password:
                    log = Logs(activity=Log.LOGIN.value, user_id=row.id)
                    session.add(log)
                    session.commit()
                else:
                    wrong_password_message = QMessageBox()
                    wrong_password_message.setText("Wrong password. Please try again")
                    wrong_password_message.exec()
                    return
                # Crete txt file with logged user.id if checkbox remember_me is checked
                if self.remember_me_checkbox.isChecked():
                    save_login(user_id=row.id)
                else:
                    try:
                        delete_login()
                    except FileNotFoundError:
                        pass
                message = QMessageBox()
                message.setText("You have logged in successfully")
                message.exec()
                self.user_id = row.id
                self.accept()

            else:
                message = QMessageBox()
                message.setText("There is no account with that email address")
                message.exec()

    def sign_in_link(self):
        sign_in = self.SignIn(self.database)
        self.setEnabled(False)
        sign_in.exec()
        self.setEnabled(True)

    def checkbox_function(self):
        if self.password_visibility_checkbox.isChecked():
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

    def cancel_button_function(self):
        self.reject()

    class SignIn(QDialog):
        def __init__(self, database):
            super().__init__()
            self.database = database
            self.layout = QGridLayout()
            self.setLayout(self.layout)

            self.label = QLabel(self)
            self.label.setText("Email Address:")
            self.layout.addWidget(self.label, 0, 0)
            self.email_input = QLineEdit(self)
            self.email_input.setPlaceholderText("Email Address")
            self.layout.addWidget(self.email_input, 0, 1)

            self.password_label = QLabel(self)
            self.password_label.setText("Password:")
            self.layout.addWidget(self.password_label, 1, 0)
            self.password_input = QLineEdit(self)
            self.password_input.setPlaceholderText("Password")
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.layout.addWidget(self.password_input, 1, 1)

            self.password_visibility_checkbox = QCheckBox(self)
            self.password_visibility_checkbox.setChecked(False)
            self.password_visibility_checkbox.setText("   Show\nPassword")
            self.layout.addWidget(self.password_visibility_checkbox, 1, 2)
            self.password_visibility_checkbox.clicked.connect(self.click_checkbox)

            self.rep_password_label = QLabel(self)
            self.rep_password_label.setText("Repeat password:")
            self.layout.addWidget(self.rep_password_label, 2, 0)
            self.rep_password_input = QLineEdit(self)
            self.rep_password_input.setPlaceholderText("Password")
            self.rep_password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.layout.addWidget(self.rep_password_input, 2, 1)

            self.create_account_button = QPushButton(self)
            self.create_account_button.setText("Create Account")
            self.layout.addWidget(self.create_account_button, 3, 0)
            self.create_account_button.clicked.connect(self.create_account_function)

            self.cancel_button = QPushButton(self)
            self.cancel_button.setText("Cancel")
            self.layout.addWidget(self.cancel_button, 3, 1)
            self.cancel_button.clicked.connect(lambda: self.reject())

        def click_checkbox(self):
            if self.password_visibility_checkbox.isChecked():
                self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            else:
                self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        def create_account_function(self):
            email = self.email_input.text()
            password = self.password_input.text()
            rep_password = self.rep_password_input.text()
            # check email validation
            em_valid, em_message = email_validation(email, self.database)
            if not em_valid:
                QMessageBox(text=f"{em_message}").exec()
                return

            # Check if password and repeat password are the same
            if password != rep_password:
                QMessageBox(text="Passwords do not match!").exec()
                return
            # Validate password for characters and length
            pas_valid, pas_message = validate_password(password)
            if pas_valid:
                hashed_password = hash_password(password)
                with self.database.session() as session:
                    new_user = Users(
                        email=email, password=hashed_password, role=Role.USER.value
                    )
                    session.add(new_user)
                    session.commit()
                    session.close()
                QMessageBox(text="Your Account has been created !!!").exec()
                self.accept()
            else:
                QMessageBox(text=f"{pas_message}").exec()


class MainWindow(QMainWindow):
    def __init__(self, database, user_id):
        super().__init__()
        self.database = database

        # Logged User form Login window
        self.user_id = user_id
        # Get iser based on id and save it in self.user variable for later use in main window
        with self.database.session() as session:
            self.user = session.get(Users, self.user_id)

        self.new_project_window = None
        self.all_projects_window = None
        self.user_window = None

        self.move(500, 250)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle("Main Window")
        self.layout = QGridLayout()
        self.central_widget.setLayout(self.layout)

        # WIDGETS
        # Welcome labe
        self.welcome_label = QLabel(self)
        self.welcome_label.setText(f"Welcome to Skaut {self.user.email}")
        self.layout.addWidget(self.welcome_label, 0, 0)
        # Create New Project Button
        self.create_button = QPushButton(self)
        self.create_button.setText("CREATE NEW PROJECT")
        self.layout.addWidget(self.create_button, 1, 0)
        self.create_button.clicked.connect(self.create_project_button)

        # Projects Button
        self.all_projects_button = QPushButton(self)
        self.all_projects_button.setText("PROJECTS")
        self.layout.addWidget(self.all_projects_button, 2, 0)
        self.all_projects_button.clicked.connect(self.all_projects_button_function)

        # User Button
        self.user_button = QPushButton(self)
        self.user_button.setText("USER DASHBOARD")
        self.layout.addWidget(self.user_button, 3, 0)
        self.user_button.clicked.connect(self.user_window_button_function)

        row_count = self.layout.rowCount()
        self.layout.setRowStretch(row_count, 1)

    def user_window_button_function(self):
        self.user_window = UserWindow(self.database, self)
        self.user_window.show()
        self.hide()

    def create_project_button(self):
        self.new_project_window = NewProjectWindow(self)
        self.hide()
        self.new_project_window.exec()
        self.show()

    def all_projects_button_function(self):
        self.all_projects_window = ProjectsWindow(self.database, self.user)
        self.hide()
        self.all_projects_window.exec()
        self.show()


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
        self.cancel_button.clicked.connect(self.close)

    def save_project(self):
        name = self.name_input.text()
        description = self.description_input.toPlainText()
        beginning_date = datetime.now()
        project_owner = self.main_window.user.email
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
                    session.flush()  # Flush to get project.id before commit

                    # Log activity in database
                    log = Logs(
                        activity=Log.CREATE_PROJECT.value,
                        user_id=self.main_window.user_id,
                        project_id=project.id,
                    )
                    session.add(log)
                    session.commit()
                success_message = QMessageBox()
                success_message.setText("Project has been created successfully")
                print("Project has been created successfully")
                success_message.exec()
                self.close()
        else:
            warning_message = QMessageBox()
            warning_message.setText("Please enter name of project and description")
            warning_message.exec()


class ProjectsWindow(QDialog):
    def __init__(self, database, user):
        super().__init__()


        self.database = database
        self.user = user
        self.single_project = None

        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setFixedHeight(200)
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area, 0, 0)

        self.container = QWidget()
        self.scroll_area.setWidget(self.container)

        self.ref_layout = QGridLayout()
        self.ref_layout.setVerticalSpacing(10)  # 10 pixels between rows
        self.ref_layout.setHorizontalSpacing(10)  # self.ref_layout.setContentsMargins(10, 10, 10, 10)  # Optional: add margins around the layout
        self.container.setLayout(self.ref_layout)


        self.refresh_layout()


        self.cancel_button = QPushButton(self)
        self.cancel_button.setText("BACK")
        self.main_layout.addWidget(self.cancel_button, 1, 0)
        self.cancel_button.clicked.connect(self.close)

    def refresh_layout(self):
        layout = self.ref_layout

        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # reset stretch
        self.ref_layout.setRowStretch(0, 0)

        with self.database.session() as session:
            table = session.query(Projects).all()

        counter = 0
        for i, row in enumerate(table):
            name_label = QLabel(self.container)
            name_label.setText(row.name)
            self.ref_layout.addWidget(name_label, i, 0)

            description_label = QLabel(self.container)
            description_label.setText(row.description)
            self.ref_layout.addWidget(description_label, i, 1)

            details_button = QPushButton("DETAILS", self.container)
            self.ref_layout.addWidget(details_button, i, 2)
            details_button.clicked.connect(partial(self.details_button_clicked, row.id))

            delete_button = QPushButton("DELETE", self.container)
            self.ref_layout.addWidget(delete_button, i, 3)
            delete_button.clicked.connect(partial(self.delete_button_clicked, row.id))

            counter += 1

        # push rows up so spacing stays consistent
        self.ref_layout.setRowStretch(counter + 1, 1)

    def delete_button_clicked(self, idx: int):
        with self.database.session() as session:
            project = session.get(Projects, idx)
            if project:
                session.delete(project)
                session.commit()
        self.refresh_layout()
    def details_button_clicked(self,idx: int):
        self.single_project = SingleProject(self.database, idx, self.user)
        self.single_project.exec()


class UserWindow(QMainWindow):
    def __init__(self, database, main_window):
        super().__init__()
        self.database = database
        self.main_window = main_window

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.setWindowTitle("User Window")
        self.layout = QGridLayout()
        self.centralWidget.setLayout(self.layout)

        # Cancel button
        self.cancel_button = QPushButton(self)
        self.cancel_button.setText("CANCEL")
        self.layout.addWidget(self.cancel_button, 0, 0)
        self.cancel_button.clicked.connect(
            lambda: (self.close(), self.main_window.show())
        )


class SingleProject(QDialog):
    def __init__(self, database, project_id, user):
        super().__init__()
        self.database = database
        self.project_id = project_id
        self.user = user
        self.layout = QGridLayout()
        self.setLayout(self.layout)




        self.name_label = QLabel(self)
        self.name_label.setText(self.user.name)
        self.layout.addWidget(self.name_label, 0, 0)
