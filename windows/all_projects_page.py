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
    QScrollArea, QFrame, QComboBox,
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


        self.combo = QComboBox()
        self.combo.addItems(["My Projects", "All Projects"])
        self.main_layout.addWidget(self.combo, 0,0,1,2)
        self.combo.currentTextChanged.connect(self.refresh_layout)



        self.scroll_area = QScrollArea(self)
        self.scroll_area.setFixedHeight(200)
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area, 1, 0, 1, 2)

        self.container = QWidget()
        self.scroll_area.setWidget(self.container)

        self.ref_layout = QGridLayout()
        self.ref_layout.setVerticalSpacing(10)  # 10 pixels between rows
        self.ref_layout.setHorizontalSpacing(10)  # self.ref_layout.setContentsMargins(10, 10, 10, 10)  # Optional: add margins around the layout
        self.container.setLayout(self.ref_layout)


        self.refresh_layout()


        self.cancel_button = QPushButton(self)
        self.cancel_button.setText("BACK")
        self.main_layout.addWidget(self.cancel_button, 2, 0)
        self.cancel_button.clicked.connect(self.stack.show_main_page)

        self.add_button = QPushButton(self)
        self.add_button.setText("ADD NEW PROJECT")
        self.main_layout.addWidget(self.add_button, 2, 1)
        self.add_button.clicked.connect(self.stack.show_new_project_page)

    def refresh_layout(self):
        layout = self.ref_layout

        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # reset stretch
        # self.ref_layout.setRowStretch(0, 0)

        with self.database.session() as session:
            if self.combo.currentText() == "My Projects":
                table = session.query(Projects).filter_by(project_owner=self.user.email).all()
            else:
                table = session.query(Projects).all()

        counter = 1
        for i, row in enumerate(table,start=1):
            name_label = QLabel(self.container)
            name_label.setText(row.name)
            self.ref_layout.addWidget(name_label, i, 0)
            self.ref_layout.setColumnStretch(0,4)

            description_label = QLabel(self.container)
            description_label.setText(row.description)
            self.ref_layout.addWidget(description_label, i, 1)
            self.ref_layout.setColumnStretch(1, 4)

            project_owner_label = QLabel(self.container)
            project_owner_label.setText(row.project_owner)
            self.ref_layout.addWidget(project_owner_label, i, 2)

            details_button = QPushButton("OPEN", self.container)
            self.ref_layout.addWidget(details_button, i, 3)
            details_button.clicked.connect(partial(self.details_button_clicked, row.id))
            self.ref_layout.setColumnStretch(2, 1)

            delete_button = QPushButton("DELETE", self.container)
            if row.project_owner != self.user.email:
                delete_button.setEnabled(False)
            self.ref_layout.addWidget(delete_button, i, 4)
            delete_button.clicked.connect(partial(self.delete_button_clicked, row.id))
            self.ref_layout.setColumnStretch(3, 1)

            counter += 1

        # push rows up so spacing stays consistent
        self.ref_layout.setRowStretch(counter + 1, 1)
        self.container.adjustSize()
        self.adjustSize()

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
        self.stack.show_single_project(idx)

