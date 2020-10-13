#! /usr/bin/env python3
import sqlite3
import sys
from time import time_ns

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
                             QLineEdit, QMainWindow, QPushButton, QScrollArea,
                             QSizePolicy, QTextEdit, QVBoxLayout, QWidget)

from icon_win import icon_taskbar
from table import hw_table


class QLabelClicked(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        QLabel.__init__(self, parent)

        self.setStyleSheet(
            """
            QLabel::hover
            {
            background-color: #414451;

            }"""
        )

    def mousePressEvent(self, env):
        self.clicked.emit()


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
        self.descrip()
        self.btns()

    def past_hw(self) -> None:
        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.vbox = QVBoxLayout()

        hw_table()
        with sqlite3.connect("employee.db") as conn:
            cur = conn.cursor()

            cur.execute("SELECT CLASS, SUBJECT, TITLE FROM HW")
            past_hw = cur.fetchall()

        self.past_hw_list = []
        for assign_class, subject, title in past_hw:
            label = QLabelClicked(f"[{assign_class}:{subject}] {title}")
            self.past_hw_list.append(label)
            self.vbox.addWidget(label)

        self.widget.setLayout(self.vbox)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.scroll.setObjectName("Scroll")

        self.generalLayout.addWidget(self.scroll, 2)

    def title(self) -> None:
        self.title_label = QLabel("Title")
        self.title_ledit = QLineEdit()

        self.vertLayout.addWidget(self.title_label)
        self.vertLayout.addWidget(self.title_ledit)

    def student_class(self) -> None:
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

    def descrip(self) -> None:
        self.descrip_label = QLabel("Description (Homework)")

        self.descrip = QTextEdit()

        self.vertLayout.addWidget(self.descrip_label)
        self.vertLayout.addWidget(self.descrip)

    def btns(self) -> None:
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
    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.view = HomeWorkUI()
        self.set_stylesheet()
        self.connectSignals()

    def connectSignals(self) -> None:
        self.view.clear.clicked.connect(self.cancel)
        self.view.ok.clicked.connect(self.ok)

        for hw in self.view.past_hw_list:
            hw.clicked.connect(lambda: print(5))

    def cancel(self) -> None:
        self.view.title_ledit.clear()
        self.view.descrip.clear()

    def ok(self) -> None:
        self.title = self.view.title_ledit.text()
        self.hw_class = self.view.class_combo_box.currentText()
        self.subject = self.view.sub_combo_box.currentText()
        self.descrip = self.view.descrip.toPlainText()

        if self.title and self.descrip:
            with sqlite3.connect("employee.db") as conn:
                conn.execute(
                    f""" INSERT INTO HW
                              VALUES( {time_ns()},
                                     "{self.title}",
                                     "{self.hw_class}",
                                     "{self.subject}",
                                     "{self.descrip}") """
                )

    def set_stylesheet(self) -> None:
        """ sets the style of widgets according to the stylesheet specified """

        with open("stylesheet.qss", "r") as qss:
            self.app.setStyleSheet(qss.read())

    def run(self) -> int:

        self.view.show()
        return self.app.exec_()


if __name__ == "__main__":
    icon_taskbar()
    window = HomeWorkCtrl()
    sys.exit(window.run())
