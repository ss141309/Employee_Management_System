#! /usr/bin/env python3
import sys
import os
import ctypes
import hashlib

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

if sys.platform == "win32":
    myappid = "abcd"  # arbitrary string

    # the following statment tells windows,
    # that the program that I am running is using Python as a host,
    # so that I can display its taskbar icon, see: https://bit.ly/3fv9kr7
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


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


class LoginUI(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("resources/icon.svg"))
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

        self.verticalSpacer1 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalSpacer2 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        # Adding Widgets and Layouts
        self.vlayout.addItem(self.verticalSpacer1)
        self.vlayout.addWidget(self.welcome_label)
        self.vlayout.addWidget(self.id_ledit)
        self.vlayout.addWidget(self.paswd_ledit)
        self.vlayout.addLayout(self.layout)
        self.vlayout.addItem(self.verticalSpacer2)

        self.generalLayout.addLayout(self.vlayout, 0, 1)


class LoginCtrl:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.view = LoginUI()

        self.connectSignals()

    def connectSignals(self):
        self.view.buttonBox.accepted.connect(self.accept)
        self.view.buttonBox.rejected.connect(self.reject)

    def accept(self):
        self.id_entered = self.view.id_ledit.text()
        self.pswd_entered = self.view.paswd_ledit.text()

        self.salt, self.key = self.hash_paswd(self.pswd_entered)

    def reject(self):
        self.view.close()

    def hash_paswd(self, password):
        # urandom generates random numbers for cryptographic use
        salt = os.urandom(32)  # salt makes it more difficult to crack passwords

        # n: iterations count
        # r: block size
        # p: parallelism factor
        # password is encoded because scrypt needs bytes
        key = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=16384, r=8, p=1)

        return (salt, key)

    def run(self):
        self.view.show()
        return self.app.exec_()


if __name__ == "__main__":
    window = LoginCtrl()
    sys.exit(window.run())
