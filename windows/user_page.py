
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QPushButton,
    QLabel,
    QLineEdit
)


class UserWindow(QWidget):
    def __init__(self, database,user, stack):
        super().__init__()
        self.database = database
        self.user = user
        self.stack = stack

        self.edit_buttons = []
        self.data_inputs = []


        self.setWindowTitle("User Window")
        self.layout = QGridLayout()
        self.setLayout(self.layout)


        self.ref_widget = QWidget(self)
        self.layout.addWidget(self.ref_widget, 0, 0)
        self.ref_layout = QGridLayout()
        self.ref_widget.setLayout(self.ref_layout)

        self.refresh_layout()

        # Cancel button
        self.cancel_button = QPushButton(self)
        self.cancel_button.setText("BACK")
        self.layout.addWidget(self.cancel_button, 1, 0)
        self.cancel_button.clicked.connect(self.handle_back_button)

    def handle_back_button(self):
        self.refresh_layout()
        self.stack.show_main_page()



        # Widgets

    def refresh_layout(self):

        layout = self.ref_layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        attributes = ["name", "surname", "phone"]
        for index, attribute in enumerate(attributes):
            self.data_row(attribute, self.user, index, layout=layout)
    # Clear old list of added buttons
        self.edit_buttons.clear()
    def data_row(self,attr, user, index, layout=None):

        data_label = QLabel()
        data_label.setText(attr+":")
        layout.addWidget(data_label, index, 0)

        data_input = QLineEdit()
        data_input.setPlaceholderText(f"Enter {attr}")
        layout.addWidget(data_input, index, 1)
        self.data_inputs.append(data_input)

        edit_button = QPushButton("Edit")
        layout.addWidget(edit_button, index, 2)
        self.edit_buttons.append(edit_button)

        save_button = QPushButton("Save")
        layout.addWidget(save_button, index, 3)
        save_button.setEnabled(False)



        number_of_data_rows = self.ref_layout.rowCount()
        self.ref_layout.setRowStretch(number_of data_rows+1, 1)
