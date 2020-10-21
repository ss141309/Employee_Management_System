# importing libraries
import sqlite3
import sys
from datetime import date
from time import time_ns

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QDateTime, Qt, pyqtSignal
from PyQt5.QtGui import QBrush, QTextCharFormat
from PyQt5.QtWidgets import (QApplication, QComboBox, QDateEdit, QFormLayout,
                             QHBoxLayout, QLabel, QLineEdit, QMainWindow,
                             QPushButton, QScrollArea, QSizePolicy, QTextEdit,
                             QVBoxLayout, QWidget)

from hw import QLabelClicked
from icon_win import icon_taskbar
from table import leave_table


class LeaveUI(QMainWindow):
    def __init__(self, emp_id) -> None:
        super().__init__()
        self.emp_id = emp_id
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self.title()
        self.leave_dates()
        self.descrip()
        self.btns()
        self.sub_leave()

    def title(self):
        self.title_label = QLabel("Title")

        self.title_ledit = QLineEdit()

        self.generalLayout.addWidget(self.title_label)
        self.generalLayout.addWidget(self.title_ledit)

    def leave_dates(self):
        self.label = QLabel("From Date")
        self.label_2 = QLabel("To Date")

        self.date = QDateEdit(calendarPopup=True)
        self.date.setDateTime(QDateTime.currentDateTime())
        self.date2 = QDateEdit(calendarPopup=True)
        self.date2.setDateTime(QDateTime.currentDateTime())

        fmt = QTextCharFormat()
        fmt.setForeground(QBrush(Qt.white))
        self.date.calendarWidget().setWeekdayTextFormat(Qt.Saturday, fmt)
        self.date2.calendarWidget().setWeekdayTextFormat(Qt.Saturday, fmt)

        self.generalLayout.addWidget(self.label)
        self.generalLayout.addWidget(self.date)

        self.generalLayout.addWidget(self.label_2)
        self.generalLayout.addWidget(self.date2)

    def descrip(self):
        self.reason_label = QLabel("Reason")

        self.leave_descrip = QTextEdit()

        self.generalLayout.addWidget(self.reason_label)
        self.generalLayout.addWidget(self.leave_descrip)

    def sub_leave(self):

        self.leave_scroll = QScrollArea()
        self.widget = QWidget()
        self.hbox = QVBoxLayout()
        self.submitted_leave = QLabel("Submitted Leaves :")

        self.widget.setLayout(self.hbox)
        self.leave_scroll.setWidget(self.widget)

        # getting the submiited leave from sql table
        leave_table()
        with sqlite3.connect("employee.db") as conn:
            cur = conn.cursor()

            cur.execute(
                """SELECT LI_ID, TITLE, FROM_DAY, FROM_MONTH, FROM_YEAR, TO_DAY, TO_MONTH, TO_YEAR FROM LEAVEINFO
                        WHERE TH_ID = ?""",
                (self.emp_id,),
            )
            sub_leave = cur.fetchall()

        # displaying the past leave in scroll area as clickable widget
        self.past_leave_list = []
        for (
            li_id,
            title,
            from_day,
            from_month,
            from_year,
            to_day,
            to_month,
            to_year,
        ) in sub_leave:
            label = QLabelClicked(
                f"[From: {from_day}-{from_month}-{from_year} -> To:{to_day}-{to_month}-{to_year}] {title}"
            )
            self.past_leave_list.append([label, li_id])
            self.hbox.addWidget(label)

        self.generalLayout.addWidget(self.submitted_leave)
        self.leave_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.leave_scroll.setWidgetResizable(True)
        self.leave_scroll.setWidget(self.widget)

        self.generalLayout.addWidget(self.leave_scroll, 2)

    def btns(self) -> None:
        """
        Add buttons to add and clear homework
        """
        self.ok = QPushButton()
        self.clear = QPushButton()

        self.ok.setText("Submit")
        self.clear.setText("Clear")

        self.empty = QWidget()
        self.empty.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.empty)
        self.hlayout.addWidget(self.ok)
        self.hlayout.addWidget(self.clear)

        self.generalLayout.addLayout(self.hlayout)


class LeaveCtrl:
    def __init__(self, emp_id) -> None:
        self.emp_id = emp_id

        self.app = QApplication(sys.argv)
        self.view = LeaveUI(self.emp_id)
        self.set_stylesheet()
        self.connectSignals()

    def connectSignals(self) -> None:
        """
        Connects signals
        """
        self.view.clear.clicked.connect(self.cancel)
        self.view.ok.clicked.connect(self.add)

        for leave in self.view.past_leave_list:
            leave[0].clicked.connect(
                lambda leave=leave: self.set_past_ui(leave[1])
            )

    def cancel(self):
        """
        Clears text in the field
        If button is named "New" connects it to the add function
        """
        self.view.title_ledit.clear()
        self.view.leave_descrip.clear()

        # if the button's text is "New", reset the fields
        if self.view.clear.text() == "New":
            self.view.title_ledit.setEnabled(True)
            self.view.date.setEnabled(True)
            self.view.date2.setEnabled(True)
            self.view.leave_descrip.setEnabled(True)
            self.view.ok.setEnabled(True)

            self.view.clear.setText("Clear")

    def get_current_text(self):

        self.leaveinfo = self.view.date.date()
        self.day = self.leaveinfo.day()
        self.month = self.leaveinfo.month()
        self.year = self.leaveinfo.year()

        self.leaveinfo2 = self.view.date2.date()
        self.day1 = self.leaveinfo.day()
        self.month1 = self.leaveinfo.month()
        self.year1 = self.leaveinfo.year()

        self.title = self.view.title_ledit.text()
        self.leave_descrip = self.view.leave_descrip.toPlainText()

    def add(self):
        """
        Adds the Leave to the database
        """
        self.get_current_text()

        # inserting the leave in sql table
        if self.title and self.leave_descrip:
            with sqlite3.connect("employee.db") as conn:
                cur = conn.cursor()
                cur.execute(
                    """ INSERT INTO LEAVEINFO
                              VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """,
                    (
                        time_ns(),
                        self.emp_id,
                        self.title,
                        self.day,
                        self.month,
                        self.year,
                        self.day1,
                        self.month1,
                        self.year1,
                        self.leave_descrip,
                    ),
                )

                # Dynamically adding new leave in scroll area
                cur.execute(
                    """SELECT LI_ID, TITLE, FROM_DAY, FROM_MONTH, FROM_YEAR, TO_DAY, TO_MONTH, TO_YEAR
                                                                            FROM LEAVEINFO ORDER BY LI_ID DESC LIMIT 1"""
                )

                (
                    li_id,
                    title,
                    from_day,
                    from_month,
                    from_year,
                    to_day,
                    to_month,
                    to_year,
                ) = cur.fetchone()
            label = QLabelClicked(
                f"[From: {from_day}-{from_month}-{from_year} -> To: {to_day}-{to_month}-{to_year}] {title}"
            )
            self.view.past_leave_list.append([label, li_id])
            self.view.hbox.addWidget(label)

            # making the newly added leave clickable
            label.clicked.connect(lambda: self.set_past_ui(leave_id))

    def get_past_leave(self, li_id: int):

        with sqlite3.connect("employee.db") as conn:
            cur = conn.cursor()

            cur.execute(
                """SELECT TITLE, FROM_DAY, FROM_MONTH, FROM_YEAR, TO_DAY, TO_MONTH, TO_YEAR, DESCRIPTION
                           FROM LEAVEINFO
                           WHERE LI_ID = ?""",
                (li_id,),
            )
            row = cur.fetchone()
            return row

    def set_past_ui(self, li_id: int) -> None:
        """
        Sets the fields non editable
        Connects to the edit function
        """
        past_leave_list = self.get_past_leave(li_id)

        # setting the fields with past hw
        self.view.title_ledit.setText(past_leave_list[0])
        self.view.date.setDate(
            date(past_leave_list[3], past_leave_list[2], past_leave_list[1])
        )
        self.view.date2.setDate(
            date(past_leave_list[6], past_leave_list[5], past_leave_list[4])
        )
        self.view.leave_descrip.setPlainText(past_leave_list[7])

        # settings the fields non-editable
        self.view.title_ledit.setEnabled(False)
        self.view.date.setEnabled(False)
        self.view.date2.setEnabled(False)
        self.view.leave_descrip.setEnabled(False)
        self.view.ok.setEnabled(False)

        # setting buttons text
        self.view.clear.setText("New")

    def set_stylesheet(self) -> None:
        """ sets the style of widgets according to the stylesheet specified """

        with open("stylesheet.qss", "r") as qss:
            self.app.setStyleSheet(qss.read())

    def run(self) -> int:

        self.view.show()
        return self.app.exec_()


if __name__ == "__main__":
    icon_taskbar()
    window = LeaveCtrl()
    sys.exit(window.run())
