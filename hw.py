#! /usr/bin/env python3
import sqlite3
import sys
from datetime import date
from time import time_ns
from typing import Tuple

from PyQt5.QtCore import QDateTime, Qt, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QComboBox, QDateEdit, QHBoxLayout,
                             QLabel, QLineEdit, QMainWindow, QPushButton,
                             QScrollArea, QSizePolicy, QTextEdit, QVBoxLayout,
                             QWidget)

from PyQt5.QtGui import QTextCharFormat, QBrush
from table import hw_table


class QLabelClicked(QLabel):
    """
    Created a clickable QLabel
    """

    clicked = pyqtSignal()

    def __init__(self, text=None):
        QLabel.__init__(self, text)

        self.setStyleSheet(
            """
            QLabel::hover
            {
            background-color: #414451;

            }"""
        )  # show colour when hovered on

    def mousePressEvent(self, env):
        self.clicked.emit()  # emit a signal when clicked


class HomeWorkUI(QMainWindow):
    """
    Sets up the UI of the HomeWork option
    """

    def __init__(self) -> None:
        super().__init__()
        self.generalLayout = QHBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self.vertLayout = QVBoxLayout()

        self.past_hw()
        self.title()
        self.student_class()
        self.subject()
        self.duedate()
        self.descrip()
        self.btns()

    def past_hw(self) -> None:
        """
        Creates a scroll area, which displays past homework
        """

        self.hw_scroll = QScrollArea()
        self.widget = QWidget()
        self.vbox = QVBoxLayout()

        hw_table()
        with sqlite3.connect("employee.db") as conn:
            cur = conn.cursor()

            cur.execute(
                "SELECT CLASS, SUBJECT, DUE_DAY, DUE_MONTH, DUE_YEAR, TITLE, HW_ID FROM HW"
            )
            past_hw = cur.fetchall()

        self.past_hw_list = []

        for (
            assign_class,
            subject,
            due_day,
            due_month,
            due_year,
            title,
            hw_id,
        ) in past_hw:
            label = QLabelClicked(
                f"{due_day}-{due_month}-{due_year} [{subject}:{assign_class}] {title}"
            )
            self.past_hw_list.append([label, hw_id])
            self.vbox.addWidget(label)

        self.widget.setLayout(self.vbox)

        self.hw_scroll.setWidgetResizable(True)
        self.hw_scroll.setWidget(self.widget)
        self.hw_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.hw_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.generalLayout.addWidget(self.hw_scroll, 2)

    def title(self) -> None:
        """
        Add title QLabel and QLineEdit
        """

        self.title_label = QLabel("Title")
        self.title_ledit = QLineEdit()

        self.vertLayout.addWidget(self.title_label)
        self.vertLayout.addWidget(self.title_ledit)

    def student_class(self) -> None:
        """
        Add a combobox to select class for homework
        """

        class_list = (
            "Pre Nursery",
            "Nursery",
            "KG",
            "I",
            "II",
            "III",
            "IV",
            "V",
            "VI",
            "VII",
            "VIII",
            "IX",
            "X",
            "XI",
            "XII",
        )

        self.class_label = QLabel("Class")

        self.class_combo_box = QComboBox()
        self.class_combo_box.addItems(class_list)

        self.vertLayout.addWidget(self.class_label)
        self.vertLayout.addWidget(self.class_combo_box)

    def subject(self) -> None:
        """
        Add a combobox to add subject to homework
        """
        subject_list = (
            "Physics",
            "Chemistry",
            "Mathematics",
            "English",
            "Computer Science",
            "Physical Education",
            "Biology",
            "Geography",
            "Accountancy",
            "Hindi",
            "Political Science",
            "History",
            "Sociology",
        )

        self.subject_label = QLabel("Subject")

        self.sub_combo_box = QComboBox()
        self.sub_combo_box.addItems(subject_list)

        self.vertLayout.addWidget(self.subject_label)
        self.vertLayout.addWidget(self.sub_combo_box)

    def duedate(self):
        """
        Adds a Due Date for the Homework
        """
        self.label = QLabel("Due Date")
        self.date = QDateEdit(calendarPopup=True)
        self.date.setDateTime(QDateTime.currentDateTime())
        fmt = QTextCharFormat()
        fmt.setForeground(QBrush(Qt.white))
        self.date.calendarWidget().setWeekdayTextFormat(Qt.Saturday, fmt)
        self.vertLayout.addWidget(self.label)
        self.vertLayout.addWidget(self.date)

    def descrip(self) -> None:
        """
        Add a QTextEdit field to add description of homework
        """
        self.descrip_label = QLabel("Description (Homework)")

        self.hw_descrip = QTextEdit()

        self.vertLayout.addWidget(self.descrip_label)
        self.vertLayout.addWidget(self.hw_descrip)

    def btns(self) -> None:
        """
        Add buttons to add and clear homework
        """
        self.ok = QPushButton()
        self.clear = QPushButton()

        self.ok.setText("Add")
        self.clear.setText("Clear")

        self.empty = QWidget()
        self.empty.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.empty)
        self.hlayout.addWidget(self.ok)
        self.hlayout.addWidget(self.clear)

        self.vertLayout.addLayout(self.hlayout)

        self.generalLayout.addLayout(self.vertLayout, 8)


class HomeWorkCtrl:
    """
    Controls HomeWorkUI
    """

    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.view = HomeWorkUI()
        self.set_stylesheet()
        self.connectSignals()

    def connectSignals(self) -> None:
        """
        Connects signals
        """
        self.view.clear.clicked.connect(self.cancel)
        self.view.ok.clicked.connect(self.add)

        for hw in self.view.past_hw_list:
            hw[0].clicked.connect(lambda hw=hw: self.set_past_ui(hw[1]))

    def cancel(self) -> None:
        """
        Clears text in the field
        If button is named "New" connects it to the add function
        """
        self.view.title_ledit.clear()
        self.view.hw_descrip.clear()

        if self.view.clear.text() == "New":
            self.view.title_ledit.setEnabled(True)
            self.view.date.setEnabled(True)
            self.view.class_combo_box.setEnabled(True)
            self.view.sub_combo_box.setEnabled(True)
            self.view.hw_descrip.setEnabled(True)

            self.view.ok.setText("Add")
            self.view.clear.setText("Clear")

            self.view.ok.clicked.disconnect()
            self.view.ok.clicked.connect(self.add)

    def get_current_text(self) -> None:
        """
        Gets the current entered text in the fields
        """
        self.title = self.view.title_ledit.text()

        self.duedate = self.view.date.date()
        self.day = self.duedate.day()
        self.month = self.duedate.month()
        self.year = self.duedate.year()

        self.hw_class = self.view.class_combo_box.currentText()
        self.subject = self.view.sub_combo_box.currentText()
        self.hw_descrip = self.view.hw_descrip.toPlainText()

    def add(self) -> None:
        """
        Adds the homework to the database
        """
        self.get_current_text()

        if self.title and self.hw_descrip:
            with sqlite3.connect("employee.db") as conn:
                cur = conn.cursor()
                cur.execute(
                    """ INSERT INTO HW
                              VALUES(?, ?, ?, ?, ?, ?, ?, ?) """,
                    (
                        time_ns(),
                        self.title,
                        self.hw_class,
                        self.subject,
                        self.day,
                        self.month,
                        self.year,
                        self.hw_descrip,
                    ),
                )

                # Dynamically adding new homework in scroll area
                cur.execute(
                    """SELECT HW_ID, TITLE, CLASS, SUBJECT, DUE_DAY, DUE_MONTH, DUE_YEAR
                                                            FROM HW ORDER BY HW_ID DESC LIMIT 1"""
                )

                (
                    hw_id,
                    title,
                    class_assigned,
                    subject,
                    due_day,
                    due_month,
                    due_year,
                ) = cur.fetchone()

            label = QLabelClicked(
                f"{due_day}-{due_month}-{due_year} [{subject}:{assign_class}] {title}"
            )
            self.view.past_hw_list.append([label, hw_id])
            self.view.vbox.addWidget(label)

            label.clicked.connect(
                lambda: self.set_past_ui(hw_id)
            )  # making the newly added hw clickable

    def edit(self, hw_id: int) -> None:
        """
        Sets the fields editable
        Connects to the update function
        """
        self.view.title_ledit.setEnabled(True)
        self.view.class_combo_box.setEnabled(True)
        self.view.date.setEnabled(True)
        self.view.sub_combo_box.setEnabled(True)
        self.view.hw_descrip.setEnabled(True)

        self.view.ok.setText("Update")

        self.view.ok.clicked.disconnect()
        self.view.ok.clicked.connect(lambda: self.update(hw_id))

    def update(self, hw_id: int) -> None:
        """
        Updates the homework
        """
        self.get_current_text()

        if self.title and self.hw_descrip:
            with sqlite3.connect("employee.db") as conn:
                cur = conn.cursor()
                cur.execute(
                    """ UPDATE HW
                            SET TITLE = ?,
                                CLASS = ?,
                                SUBJECT = ?,
                                DUE_DAY = ?,
                                DUE_MONTH = ?,
                                DUE_YEAR = ?,
                                DESCRIPTION = ?
                       WHERE HW_ID = ?""",
                    (
                        self.title,
                        self.hw_class,
                        self.subject,
                        self.day,
                        self.month,
                        self.year,
                        self.hw_descrip,
                        hw_id,
                    ),
                )

                # Dynamically updating homework in scroll area
                cur.execute(
                    """SELECT TITLE, CLASS, SUBJECT, DUE_DAY, DUE_MONTH, DUE_YEAR
                                   FROM HW WHERE HW_ID = ?""",
                    (hw_id,),
                )

                (
                    title,
                    class_assigned,
                    subject,
                    due_day,
                    due_month,
                    due_year,
                ) = cur.fetchone()

            for i in self.view.past_hw_list:
                if i[1] == hw_id:
                    i[0].setText(
                        f"{due_day}-{due_month}-{due_year} [{subject}:{class_assigned}] {title}"
                    )

    def get_past_hw(self, hw_id: int) -> Tuple[str, str, str, str]:
        """
        Gets the hw title, class, subject and description
        """
        with sqlite3.connect("employee.db") as conn:
            cur = conn.cursor()

            cur.execute(
                """SELECT TITLE, CLASS, SUBJECT, DUE_DAY, DUE_MONTH, DUE_YEAR, DESCRIPTION
                           FROM HW
                           WHERE HW_ID = ?""",
                (hw_id,),
            )
            row = cur.fetchone()

        return row

    def set_past_ui(self, hw_id: int):
        """
        Sets the fields non editable
        Connects to the edit function
        """
        past_hw_list = self.get_past_hw(hw_id)

        self.view.title_ledit.setText(past_hw_list[0])
        self.view.class_combo_box.setCurrentText(past_hw_list[1])
        self.view.sub_combo_box.setCurrentText(past_hw_list[2])
        self.view.date.setDate(
            date(past_hw_list[5], past_hw_list[4], past_hw_list[3])
        )
        self.view.hw_descrip.setPlainText(past_hw_list[6])

        self.view.title_ledit.setEnabled(False)
        self.view.class_combo_box.setEnabled(False)
        self.view.sub_combo_box.setEnabled(False)
        self.view.date.setEnabled(False)
        self.view.hw_descrip.setEnabled(False)

        self.view.ok.setText("Edit")
        self.view.clear.setText("New")

        self.view.ok.clicked.disconnect()
        self.view.ok.clicked.connect(lambda: self.edit(hw_id))

    def set_stylesheet(self) -> None:
        """ sets the style of widgets according to the stylesheet specified """

        with open("stylesheet.qss", "r") as qss:
            self.app.setStyleSheet(qss.read())

    def run(self) -> int:

        self.view.show()
        return self.app.exec_()


if __name__ == "__main__":
    window = HomeWorkCtrl()
    sys.exit(window.run())
