# importing libraries
import sqlite3
import sys
from time import time_ns
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QDateTime, Qt, pyqtSignal
from PyQt5.QtGui import QBrush, QTextCharFormat
from PyQt5.QtWidgets import (QApplication, QComboBox, QDateEdit, QFormLayout,
                             QHBoxLayout, QLabel, QLineEdit, QMainWindow,
                             QPushButton, QScrollArea, QSizePolicy, QTextEdit,
                             QVBoxLayout, QWidget)

from icon_win import icon_taskbar
from table import leave_table
from hw import QLabelClicked


class LeaveUI(QMainWindow):

    def __init__(self, emp_id) -> None:

        super().__init__()
        self.emp_id = emp_id
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        self.form = QFormLayout()
        
        self.leaveinfo()
        self.title()
        self.btns()
        self.sub_leave()

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
                """SELECT LI_ID, FROM_DAY, FROM_MONTH, FROM_YEAR, TO_DAY, TO_MONTH, TO_YEAR, DESCRIPTION FROM LEAVEINFO
                        WHERE TH_ID = ?""", (self.emp_id,)
            )
            sub_leave = cur.fetchall()
            

        # displaying the past leave in scroll area as clickable widget
        self.past_leave_list = []
        for (
            li_id,
            from_day,
            from_month,
            from_year,
            to_day,
            to_month,
            to_year,
            description,
        ) in sub_leave:
            label = QLabelClicked(
                f"[From: {from_day}-{from_month}-{from_year} -> To:{to_day}-{to_month}-{to_year}] {description}"
            )
            self.past_leave_list.append([label, li_id])
            self.hbox.addWidget(label)
        

        self.generalLayout.addWidget(self.submitted_leave)
        self.leave_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.leave_scroll.setWidgetResizable(True)
        self.leave_scroll.setWidget(self.widget)

        self.generalLayout.addWidget(self.leave_scroll, 2)
        
    def title(self):

        self.reason_label = QLabel("Reason")

        self.leave_descrip = QTextEdit()

        self.generalLayout.addWidget(self.reason_label)
        self.generalLayout.addWidget(self.leave_descrip)

    def leaveinfo(self):

        self.label = QLabel("From Date")
        self.label_2 = QLabel("To Date")

        self.date = QDateEdit(calendarPopup=True)
        self.date.setDateTime(QDateTime.currentDateTime())
        self.date2 = QDateEdit(self,calendarPopup=True)
        self.date2.setDateTime(QDateTime.currentDateTime())

        fmt = QTextCharFormat()
        fmt.setForeground(QBrush(Qt.white))
        self.date.calendarWidget().setWeekdayTextFormat(Qt.Saturday, fmt)
        self.date2.calendarWidget().setWeekdayTextFormat(Qt.Saturday, fmt)

        self.form.addRow(self.label, self.date)
        self.form.addRow(self.label_2, self.date2)
        self.generalLayout.addLayout(self.form)
      
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

    def cancel(self):
        """
        Clears text in the field
        If button is named "New" connects it to the add function
        """

        self.view.leave_descrip.clear()

    def get_current_text(self):

        self.leaveinfo = self.view.date.date()
        self.day = self.leaveinfo.day()
        self.month = self.leaveinfo.month()
        self.year = self.leaveinfo.year()

        self.leaveinfo2 = self.view.date2.date()
        self.day1 = self.leaveinfo.day()
        self.month1 = self.leaveinfo.month()
        self.year1 = self.leaveinfo.year()

        self.leave_descrip = self.view.leave_descrip.toPlainText()

    def add(self):
        """
        Adds the Leave to the database
        """
        self.get_current_text()

        #inserting the leave in sql table
        if self.leaveinfo and self.leaveinfo2 and self.leave_descrip:
            with sqlite3.connect("employee.db") as conn:
                cur = conn.cursor()
                cur.execute(
                    """ INSERT INTO LEAVEINFO
                              VALUES(?,?,?,?,?,?,?,?,?) """,
                    (
                        time_ns(),
                        self.emp_id,
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
                    """SELECT LI_ID, TH_ID, FROM_DAY, FROM_MONTH, FROM_YEAR, TO_DAY, TO_MONTH, TO_YEAR, DESCRIPTION
                                                                            FROM LEAVEINFO ORDER BY LI_ID DESC LIMIT 1"""
                )

                (
                    li_id,
                    emp_id,
                    from_day,
                    from_month,
                    from_year,
                    to_day,
                    to_month,
                    to_year,
                    description,
                    
                ) = cur.fetchone()
            label = QLabelClicked(
                f"[{from_day}{from_month}{from_year}:{to_day}{to_month}{to_year}] {description}"
            )
            self.view.past_leave_list.append([label,li_id])
            self.view.hbox.addWidget(label)

            # making the newly added leave clickable

    
    def get_past_leave(self, emp_id: int):

        with sqlite3.connect("employee.db") as conn:
            cur = conn.cursor()

            cur.execute(
                 """SELECT LI_ID, TH_ID, FROM_DAY, FROM_MONTH, FROM_YEAR, TO_DAY, TO_MONTH, TO_YEAR, DESCRIPTION
                           FROM LEAVEINFO
                           WHERE TH_ID = ?""",
                (self.emp_id,),
            )
            row = cur.fetchone()
            print(row)


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