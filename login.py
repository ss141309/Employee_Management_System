from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys


class Login(QDialog):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #282a36;")
        self.setWindowTitle("Login")
        self.setFixedSize(1200, 750)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        self.generalLayout = QGridLayout()

        self.setLayout(self.generalLayout)

        self.login_banner()
        self.entry()

    def login_banner(self):
        frame = QWidget()
        label_Image = QLabel(frame)
        image_path = "resources/Login.png"  # path to your image file
        image_profile = QImage(image_path)  # QImage object
        label_Image.setPixmap(QPixmap.fromImage(image_profile))

        self.generalLayout.addWidget(label_Image, 0, 0)

    def entry(self):
        self.vlayout = QVBoxLayout()

        # Welcome Label
        self.welcome_label = QLabel("Welcome Back!")
        self.welcome_label.setFont(QFont("Arial", 50))
        self.welcome_label.setStyleSheet("color: white;")

        # Login
        self.id_ledit = QLineEdit()
        self.id_ledit.setPlaceholderText("Enter ID")
        self.user_tie = QIcon("resources/user-circle.svg")
        self.id_ledit.addAction(self.user_tie, QLineEdit.LeadingPosition)
        self.id_ledit.setFrame(0)
        self.id_ledit.setStyleSheet("background-color: #44475a;color: white;")

        # Password
        self.paswd_ledit = PasswordEdit()
        self.paswd_ledit.setPlaceholderText("Enter Password")
        self.paswd_ledit.setFrame(0)
        self.key_ico = QIcon("resources/key.svg")
        self.paswd_ledit.addAction(self.key_ico, QLineEdit.LeadingPosition)
        self.paswd_ledit.setEchoMode(QLineEdit.Password)

        # Buttons
        self.btns = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(self.btns)
        self.buttonBox.button(QDialogButtonBox.Ok).setStyleSheet(
            "background: #44475a;color: white;"
        )
        self.buttonBox.button(QDialogButtonBox.Cancel).setStyleSheet(
            "background: #44475a;color: white;"
        )
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.buttonBox)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        # Adding Widgets and Layouts
        self.vlayout.addItem(self.verticalSpacer)
        self.vlayout.addWidget(self.welcome_label)
        self.vlayout.addWidget(self.id_ledit)
        self.vlayout.addWidget(self.paswd_ledit)
        self.vlayout.addLayout(self.layout)
        self.vlayout.addItem(self.verticalSpacer)

        self.generalLayout.addLayout(self.vlayout, 0, 1)


class PasswordEdit(QLineEdit):
    def __init__(self, show_visibility=True):
        super().__init__()

        self.visibleIcon = QIcon("resources/eye.svg")
        self.hiddenIcon = QIcon("resources/hidden.svg")
        self.setStyleSheet("background-color: #44475a;color: white;")

        self.setEchoMode(QLineEdit.Password)

        if show_visibility:
            self.togglepasswordAction = self.addAction(
                self.visibleIcon, QLineEdit.TrailingPosition
            )
            self.togglepasswordAction.triggered.connect(self.on_toggle_password_Action)

        self.password_shown = False

    def on_toggle_password_Action(self):
        if not self.password_shown:
            self.setEchoMode(QLineEdit.Normal)
            self.password_shown = True
            self.togglepasswordAction.setIcon(self.hiddenIcon)
        else:
            self.setEchoMode(QLineEdit.Password)
            self.password_shown = False
            self.togglepasswordAction.setIcon(self.visibleIcon)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec())
