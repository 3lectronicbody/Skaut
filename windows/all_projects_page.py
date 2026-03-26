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
    QScrollArea, QHBoxLayout, QComboBox,
)
from datetime import datetime
from models import Projects, ProjectDetails, Users, Role, Logs, Log
from PySide6.QtGui import Qt
from functools import partial

class ProjectsWindow(QWidget):
    def __init__(self, database, user, stack):
        super().__init__()


        self.database = database
        self.user = user
        self.stack = stack
        self.single_project = None

        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)

        self.combo = QComboBox(self)
        self.combo.addItems(["All Projects", "My Projects"])
        self.main_layout.addWidget(self.combo, 0, 0)
        self.combo.currentIndexChanged.connect(self.combo_change)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setFixedHeight(200)
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area, 1, 0)

        self.container = QWidget()
        self.scroll_area.setWidget(self.container)

        self.ref_layout = QGridLayout()
        self.ref_layout.setVerticalSpacing(10)  # 10 pixels between rows
        self.ref_layout.setHorizontalSpacing(10)  # self.ref_layout.setContentsMargins(10, 10, 10, 10)  # Optional: add margins around the layout
        self.container.setLayout(self.ref_layout)


        self.refresh_layout(flag="All")

        # Move main_layout widgets (combo, scroll area) up and navigation buttons down
        self.main_layout.setRowStretch(2, 1)

        self.buttons_layout = QHBoxLayout()
        self.main_layout.addLayout(self.buttons_layout,3,0)

        self.back_button = QPushButton(self)
        self.back_button.setText("BACK")
        self.buttons_layout.addWidget(self.back_button)
        self.back_button.clicked.connect(self.stack.show_main_page)

        self.new_project_button = QPushButton(self)
        self.new_project_button.setText("NEW PROJECT")
        self.buttons_layout.addWidget(self.new_project_button)
        self.new_project_button.clicked.connect(self.stack.show_new_project_page)



    def refresh_layout(self, flag=None):
        layout = self.ref_layout

        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # reset stretch
        self.ref_layout.setRowStretch(0, 0)

        with self.database.session() as session:
            if flag == "All":
                table = session.query(Projects).all()
            elif flag == "My":
                table = session.query(Projects).filter_by(project_owner=self.user.email).all()
            else:
                table = session.query(Projects).all()


        counter = 0
        for i, row in enumerate(table):
            name_label = QLabel(self.container)
            name_label.setText(row.name)
            self.ref_layout.addWidget(name_label, i, 0)

            description_label = QLabel(self.container)
            description_label.setText(row.description)
            description_label.setWordWrap(True)
            description_label.setFixedWidth(100)
            description_label.setToolTip(f"{row.description}")
            self.ref_layout.addWidget(description_label, i, 1)

            project_owner_label = QLabel(self.container)
            project_owner_label.setText(row.project_owner)
            self.ref_layout.addWidget(project_owner_label, i, 2)

            details_button = QPushButton("OPEN", self.container)
            self.ref_layout.addWidget(details_button, i, 3)
            details_button.clicked.connect(partial(self.details_button_clicked, row.id))


            delete_button = QPushButton("DELETE", self.container)
            if self.user.email != project_owner_label.text():
                delete_button.setEnabled(False)
            self.ref_layout.addWidget(delete_button, i, 4)
            delete_button.clicked.connect(partial(self.delete_button_clicked, row.id))

            counter += 1

        # push rows up so spacing stays consistent
        self.ref_layout.setRowStretch(counter + 1, 1)

    def delete_button_clicked(self, idx: int):
        with self.database.session() as session:
            project = session.get(Projects, idx)
            if project:
                warning_message = QMessageBox()
                warning_message.setWindowTitle("Warning")
                warning_message.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                warning_message.setText("Are you sure you want to delete this project?")
                if warning_message.exec() == QMessageBox.StandardButton.Yes:
                    session.delete(project)
                    log = Logs(activity=Log.DELETE_PROJECT.value, user_id=self.user.id, project_id=idx)
                    session.add(log)
                    session.commit()
                    self.refresh_layout()



    def details_button_clicked(self, idx: int):
        print("clicked details button for project id")
        self.stack.show_single_project(idx)
    def combo_change(self):
        if self.combo.currentText() == "All Projects":
            self.refresh_layout(flag="All")
        elif self.combo.currentText() == "My Projects":
            self.refresh_layout(flag="My")

