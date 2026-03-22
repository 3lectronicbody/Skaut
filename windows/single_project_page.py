from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QPushButton,
    QLabel, QHBoxLayout, QVBoxLayout
)
from PySide6.QtCore import Qt
from models import Projects


class SingleProject(QWidget):
    def __init__(self, database, user, project_id, stack):
        super().__init__()
        self.database = database
        self.user = user
        self.project_id = project_id
        self.stack = stack

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.name_label = QLabel(self)
        self.name_label.setText(self.user.name)
        self.layout.addWidget(self.name_label, 0, Qt.AlignmentFlag.AlignCenter)

        self.project_name_label = QLabel(self)
        self.project_name_label.setText("load project name here")
        self.layout.addWidget(self.project_name_label, 0, Qt.AlignmentFlag.AlignCenter)

        # self.layout.setStretch(1,1)

        self.button_layout = QHBoxLayout()
        self.layout.addLayout(self.button_layout)

        self.back_button = QPushButton(self)
        self.back_button.setText("Back")
        self.button_layout.addWidget(self.back_button, 0, Qt.AlignmentFlag.AlignCenter)
        self.back_button.clicked.connect(self.stack.show_all_projects_page)

    def load_project(self, project_id):
        with self.database.session() as session:
            loaded_project = session.get(Projects, project_id)
        if loaded_project:
            self.project_name_label.setText(loaded_project.name)







