#! /usr/bin/env python3
import sqlite3
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QImage, QPixmap
from PyQt5.QtSvg import QGraphicsSvgItem
from PyQt5.QtWidgets import (QApplication, QGraphicsScene, QGraphicsView,
                             QGridLayout, QHBoxLayout, QLabel, QMainWindow,
                             QVBoxLayout, QWidget)



class InfoCard(QWidget):
    """
    Custom Widget which displays an icon
    alongside title and its value in a box
    """

    def __init__(self, vector_path: str, title: str, value: str) -> None:
        super().__init__()
        self.generalLayout = QHBoxLayout()
        self.setLayout(self.generalLayout)
        self.setStyleSheet(
            "QWidget {border: 1px solid white; border-radius: 8px;}"
        )

        self.vlayout = QVBoxLayout()

        self.vector_path = vector_path
        self.title = title
        self.value = value

        self.icon()
        self.info()

    def icon(self) -> None:
        """
        Displays the icon in the box
        """
        self.svgItem = QGraphicsSvgItem(self.vector_path)
        self.svgItem.setScale(0.07)  # minimizing the svg

        self.scene = QGraphicsScene()
        self.scene.addItem(self.svgItem)

        self.view = QGraphicsView()
        self.view.setScene(self.scene)

        self.generalLayout.addWidget(self.view, 1)

    def info(self) -> None:
        """
        Displaying the title and value
        """
        self.title_label = QLabel(self.title)
        self.value_label = QLabel(self.value)

        self.vlayout.addWidget(self.title_label)
        self.vlayout.addWidget(self.value_label)

        self.generalLayout.addLayout(self.vlayout, 5)


class DashBoardUI(QMainWindow):
    """
    Sets up the UI of the HomeWork option
    """

    def __init__(self, emp_id: str) -> None:
        super().__init__()
        self.generalLayout = QGridLayout()
        self._centralWidget = QWidget()
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self.emp_id = emp_id

        self.get_info()
        self.profile_img()
        self.greet_user()
        self.info()

    def profile_img(self, img_path: str = "gerwinski-gnu-head.png") -> None:
        """
        Displaying the profile picture
        """
        frame = QWidget()
        label_Image = QLabel(frame)

        image_path = img_path
        image_profile = QImage(image_path)
        image_profile = image_profile.scaled(
            250,
            250,
            aspectRatioMode=Qt.KeepAspectRatio,
            transformMode=Qt.SmoothTransformation,
        )  # To scale image and keep its Aspect Ratio

        label_Image.setPixmap(QPixmap.fromImage(image_profile))

        self.generalLayout.addWidget(label_Image, 0, 0)

    def get_info(self) -> None:
        """
        Gets the teacher's info
        """
        with sqlite3.connect("employee.db") as conn:
            cur = conn.cursor()

            cur.execute(
                """ SELECT FIRST_NAME,
                           LAST_NAME,
                           CONTACT,
                           EMAIL,
                           DOB_DAY,
                           DOB_MONTH,
                           DOB_YEAR,
                           JOINING_DAY,
                           JOINING_MONTH,
                           JOINING_YEAR,
                           CLASSES_ASSIGNED,
                           SUBJECTS,
                           BUS_ROUTE,
                           ADDRESS
                           FROM EMPL WHERE EMP_ID=?""",
                (self.emp_id,),
            )

            (
                self.first_name,
                self.last_name,
                self.contact,
                self.email,
                self.dob_day,
                self.dob_month,
                self.dob_year,
                self.join_day,
                self.join_month,
                self.join_year,
                self.classes,
                self.subjects,
                self.bus,
                self.address,
            ) = cur.fetchone()

    def greet_user(self) -> None:
        """
        Displays a Welcome Back! greeting to the user
        """
        self.vlayout = QVBoxLayout()

        # Welcome Label
        self.welcome_label = QLabel("Welcome Back!")
        self.welcome_label.setFont(QFont("Arial", 50))

        # Name Label
        self.name_label = QLabel(self.first_name)
        self.name_label.setFont(QFont("Arial", 45))

        # Adding Widgets and Layouts
        self.vlayout.addWidget(self.welcome_label)
        self.vlayout.addWidget(self.name_label)

        self.generalLayout.addLayout(self.vlayout, 0, 1)

    def info(self) -> None:
        """
        Setting up the info cards in a layout
        """
        self.info_grid = QGridLayout()

        self.name_card = InfoCard(
            "resources/user.svg", "Name", f"{self.first_name} {self.last_name}"
        )
        self.info_grid.addWidget(self.name_card, 0, 0)

        self.contact_card = InfoCard(
            "resources/mobile-alt.svg", "Contact", self.contact
        )
        self.info_grid.addWidget(self.contact_card, 0, 1)

        self.email_card = InfoCard(
            "resources/envelope.svg", "Email", self.email
        )
        self.info_grid.addWidget(self.email_card, 0, 2)

        self.dob_card = InfoCard(
            "resources/calendar-day.svg",
            "Date of Birth",
            f"{self.dob_day}-{self.dob_month}-{self.dob_year}",
        )
        self.info_grid.addWidget(self.dob_card, 1, 0)

        self.joining_date_card = InfoCard(
            "resources/calendar-alt.svg",
            "Joining Date",
            f"{self.join_day}-{self.join_month}-{self.join_year}",
        )
        self.info_grid.addWidget(self.joining_date_card, 1, 1)

        self.classes_assigned_card = InfoCard(
            "resources/chalkboard-teacher.svg",
            "Classes Assigned",
            "XII-(A, B, C), XI-(A), X-(B)",
        )
        self.info_grid.addWidget(self.classes_assigned_card, 1, 2)

        self.subjects_card = InfoCard(
            "resources/book.svg", "Subjects Assigned", self.subjects
        )
        self.info_grid.addWidget(self.subjects_card, 2, 0)

        self.bus_route_card = InfoCard(
            "resources/bus-alt.svg", "Bus Route", self.bus
        )
        self.info_grid.addWidget(self.bus_route_card, 2, 1)

        self.address_card = InfoCard(
            "resources/address-book.svg",
            "Address",
            self.address,
        )
        self.info_grid.addWidget(self.address_card, 2, 2)

        self.generalLayout.addLayout(self.info_grid, 1, 0, 5, 5)


class DashBoardCtrl:
    """
    Controls HomeWorkUI
    """

    def __init__(self, emp_id: str) -> None:
        self.app = QApplication(sys.argv)
        self.view = DashBoardUI(emp_id)
        self.set_stylesheet()

    def set_stylesheet(self) -> None:
        """ sets the style of widgets according to the stylesheet specified """

        with open("stylesheet.qss", "r") as qss:
            self.app.setStyleSheet(qss.read())

    def run(self) -> int:

        self.view.show()
        return self.app.exec_()


if __name__ == "__main__":
    window = DashBoardCtrl()
    sys.exit(window.run())
