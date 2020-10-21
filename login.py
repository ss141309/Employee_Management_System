#! /usr/bin/env python3
import hashlib
import os
import sqlite3
import sys
from typing import Tuple, Union

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QImage, QPixmap
from PyQt5.QtWidgets import (QApplication, QDialog, QDialogButtonBox,
                             QGridLayout, QLabel, QLineEdit, QSizePolicy,
                             QSpacerItem, QVBoxLayout, QWidget)

from icon_win import icon_taskbar
from menu import MainCtrl


class PasswordEdit(QLineEdit):
    """
    Can toggle password visibility
    """

    def __init__(self, show_visibility: bool = True) -> None:
        super().__init__()

        # icons for show/hide password
        self.visibleIcon = QIcon("resources/eye.svg")
        self.hiddenIcon = QIcon("resources/hidden.svg")

        self.setEchoMode(QLineEdit.Password)  # to hide the password

        if show_visibility:
            self.togglepasswordAction = self.addAction(
                self.visibleIcon, QLineEdit.TrailingPosition
            )  # adding the visibleIcon to QLineEdit
            self.togglepasswordAction.triggered.connect(
                self.on_toggle_password_Action
            )

        self.password_shown = False

    def on_toggle_password_Action(self) -> None:
        """
        Toggles between show/hide password
        """
        if not self.password_shown:
            self.setEchoMode(QLineEdit.Normal)  # show the password
            self.password_shown = True
            self.togglepasswordAction.setIcon(self.hiddenIcon)
        else:
            self.setEchoMode(QLineEdit.Password)
            self.password_shown = False
            self.togglepasswordAction.setIcon(self.visibleIcon)


class LoginUI(QDialog):
    """
    Sets up the UI of the login Window
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowIcon(
            QIcon("resources/icon.svg")
        )  # setting up taskbar and window icon
        self.setWindowTitle("Login")
        self.setFixedSize(1200, 750)
        self.setWindowFlag(
            Qt.WindowMinimizeButtonHint, True
        )  # showing minimize button in the window
        self.setWindowFlag(
            Qt.WindowMaximizeButtonHint, True
        )  # showing maximize button in the window

        self.generalLayout = QGridLayout()

        self.setLayout(self.generalLayout)

        self.login_banner()
        self.entry()

    def login_banner(self) -> None:
        """
        Displays the login banner present in the left side of the window
        """
        label_Image = QLabel()
        image_path = "resources/Login.png"  # path to your image file
        image_profile = QPixmap(
            image_path
        )  # QPixmap object, QPixmap is optimized to display images
        label_Image.setPixmap(image_profile)  # adding the image to the label

        self.generalLayout.addWidget(label_Image, 0, 0)

    def entry(self) -> None:
        """
        Sets up a welcome text, an id and password line edit,
        QDialogButtonBox buttons to the window and also applies
        spacers to centre these widgets
        """
        self.vlayout = QVBoxLayout()

        # Welcome Label
        self.welcome_label = QLabel("Welcome Back!")
        self.welcome_label.setFont(QFont("Arial", 50))

        # Warning Label
        self.wrong_paswd_label = QLabel(
            "Wrong ID or Password entered! Try again"
        )
        self.wrong_paswd_label.setStyleSheet("color: red")

        # Login
        self.id_ledit = QLineEdit()
        self.id_ledit.setPlaceholderText("Enter ID")
        self.user_tie = QIcon("resources/user-circle.svg")
        self.id_ledit.addAction(self.user_tie, QLineEdit.LeadingPosition)

        # Password
        self.paswd_ledit = PasswordEdit()
        self.paswd_ledit.setPlaceholderText("Enter Password")
        self.key_ico = QIcon("resources/key.svg")
        self.paswd_ledit.addAction(self.key_ico, QLineEdit.LeadingPosition)
        self.paswd_ledit.setEchoMode(QLineEdit.Password)

        # Buttons
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(
            "Login", QDialogButtonBox.AcceptRole
        ).setToolTip("Logins into the application")
        self.buttonBox.addButton(
            "Close", QDialogButtonBox.RejectRole
        ).setToolTip("Closes the application")
        self.vert_layout = QVBoxLayout()
        self.vert_layout.addWidget(self.buttonBox)

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
        self.vlayout.addWidget(self.wrong_paswd_label)
        self.vlayout.addLayout(self.vert_layout)
        self.vlayout.addItem(self.verticalSpacer2)

        self.wrong_paswd_label.hide()

        self.generalLayout.addLayout(self.vlayout, 0, 1)


class LoginCtrl:
    """ Class to control the Login window """

    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.view = LoginUI()

        self.connectSignals()
        self.set_stylesheet()

    def connectSignals(self) -> None:
        """
        connects signals
        """
        self.view.buttonBox.accepted.connect(self.accept_creds)
        self.view.buttonBox.rejected.connect(self.reject)

    def accept_creds(self) -> None:
        """
        Gets the id and password entered
        Checks if the password entered is correct
        and user id is not left empty
        """
        # getting the entered text from the id and password line edit
        self.id_entered = self.view.id_ledit.text()
        self.pswd_entered = self.view.paswd_ledit.text()

        if self.id_entered and self.check_paswd(
            self.id_entered, self.pswd_entered
        ):
            self.right_entries()
        else:
            self.wrong_entries()

    def reject(self) -> None:
        """ Closes the window when Cancel button is presses """
        self.view.close()

    def hash_paswd(
        self, password: Union[str, bytes], salt: bytes = os.urandom(32)
    ) -> Tuple[bytes, bytes]:
        """
        Hashes the password for secure storage
        uses scrypt hashing method, which is present in the hashlib library
        urandom generates random numbers for cryptographic use
        salt makes it more difficult to crack password
        returns the salt and the key
        """
        if not isinstance(
            password, bytes
        ):  # checking if password is bytes object or not
            password = password.encode("utf-8")

        # n: iterations count
        # r: block size
        # p: parallelism factor
        # password is encoded because scrypt needs bytes
        key = hashlib.scrypt(password, salt=salt, n=16384, r=8, p=1)

        return (salt, key)

    def check_paswd(self, user_id: str, passwd: str) -> bool:
        """
        Checks the password entered against the password in the SQL table
        returns True or False
        """
        with sqlite3.connect("employee.db") as conn:
            cur = conn.cursor()

            cur.execute(
                f"""SELECT PASSWORD, SALT FROM EMPL
                               WHERE EMP_ID = "{user_id}" """
            )
            stored_passwd, stored_salt = cur.fetchone()

        return self.hash_paswd(passwd, stored_salt)[1] == stored_passwd

    def wrong_entries(self) -> None:
        """
        Colours the entry boxes red for wrong entries
        also, displays a text notifying the user
        """
        self.view.paswd_ledit.setStyleSheet("border: 0.5px solid red;")
        self.view.id_ledit.setStyleSheet("border: 0.5px solid red;")
        self.view.wrong_paswd_label.show()

    def right_entries(self) -> None:
        """
        Reverts the entry box back to grey for right entry
        also hides the error text, if present
        """
        self.view.paswd_ledit.setStyleSheet("border: solid grey;")
        self.view.id_ledit.setStyleSheet("border: 0.5px solid grey;")
        self.view.wrong_paswd_label.hide()
        self.view.accept()

    def set_stylesheet(self) -> None:
        """ sets the style of widgets according to the stylesheet specified """

        with open("stylesheet.qss", "r") as qss:
            self.app.setStyleSheet(qss.read())

    def run(self) -> int:
        self.view.show()
        return self.view.exec_()


if __name__ == "__main__":
    icon_taskbar()
    window = LoginCtrl()
    if (
        window.run() == QDialog.Accepted
    ):  # opening the main menu if password is correct
        main_menu = MainCtrl(window.id_entered)
        sys.exit(main_menu.run())
