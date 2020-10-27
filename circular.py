import sqlite3
import sys

from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtGui import QBrush, QIcon, QTextCharFormat
from PyQt5.QtWidgets import (QApplication, QDateEdit, QFormLayout, QHBoxLayout,
                             QLabel, QLineEdit, QMainWindow, QPushButton,
                             QScrollArea, QSizePolicy, QToolButton,
                             QVBoxLayout, QWidget)

from table import circular_table


class CollapsibleBox(QWidget):
    def __init__(self, title: str) -> None:
        super().__init__()
        self.generalLayout = QVBoxLayout()
        self.setLayout(self.generalLayout)

        self.toggle_button = QToolButton(
            text=title, checkable=True, checked=False
        )
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(Qt.RightArrow)
        self.toggle_button.pressed.connect(self.on_pressed)

        self.content_area = QScrollArea()
        self.content_area.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed
        )

        self.generalLayout.addWidget(self.toggle_button)
        self.generalLayout.addWidget(self.content_area)

    def on_pressed(self) -> None:
        checked = self.toggle_button.isChecked()
        self.toggle_button.setArrowType(
            Qt.DownArrow if not checked else Qt.RightArrow
        )
        if self.content_widget.isVisible():
            self.content_area.hide()
        else:
            self.content_area.show()

    def setContent(self, content: str) -> None:
        self.content = QLabel(content)
        self.content_layout = QVBoxLayout()
        self.content_layout.addWidget(self.content)
        self.content_widget = QWidget()
        self.content_widget.setLayout(self.content_layout)
        self.content_area.setWidget(self.content_widget)
        self.content_area.hide()


class Filter(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.generalLayout = QHBoxLayout()
        self.setLayout(self.generalLayout)

        self.date()
        self.btn()

    def date(self) -> None:
        """
        Displays "From" and "To" labels and QDateEdits
        """
        self.form_layout1 = QFormLayout()
        self.form_layout2 = QFormLayout()

        self.from_label = QLabel("From: ")
        self.to_label = QLabel("To: ")

        self.date = QDateEdit(calendarPopup=True)
        self.date.setDateTime(QDateTime.currentDateTime())
        self.date2 = QDateEdit(self, calendarPopup=True)
        self.date2.setDateTime(QDateTime.currentDateTime())

        fmt = QTextCharFormat()
        fmt.setForeground(QBrush(Qt.white))
        self.date.calendarWidget().setWeekdayTextFormat(Qt.Saturday, fmt)
        self.date2.calendarWidget().setWeekdayTextFormat(Qt.Saturday, fmt)

        self.form_layout1.addRow(self.from_label, self.date)
        self.form_layout2.addRow(self.to_label, self.date2)

        self.generalLayout.addLayout(self.form_layout1, 10)
        self.generalLayout.addLayout(self.form_layout2, 10)

    def btn(self) -> None:
        """
        Displays "Ok" and "Clear" button
        """
        self.ok_btn = QPushButton()
        self.ok_btn.setText("Ok")

        self.clear_btn = QPushButton()
        self.clear_btn.setText("Clear")

        self.generalLayout.addWidget(self.ok_btn)
        self.generalLayout.addWidget(self.clear_btn)


class CircularUI(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self.search_bar()
        self.collapsible_circular()

    def search_bar(self) -> None:
        """
        Displays a search bar with search and filter icon
        """
        self.search_ledit = QLineEdit()
        self.search_ledit.setPlaceholderText("Search")

        self.search_ledit.addAction(
            QIcon("resources/search.svg"), QLineEdit.LeadingPosition
        )
        self.filter_icon = self.search_ledit.addAction(
            QIcon("resources/filter.svg"), QLineEdit.TrailingPosition
        )

        self.filter_data = Filter()
        self.generalLayout.addWidget(self.search_ledit)
        self.generalLayout.addWidget(self.filter_data)

        self.filter_data.hide()

    def collapsible_circular(self) -> None:
        """
        Displays circulars in scroll area
        """
        self.scroll_area = QScrollArea()

        self.scroll_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_widget)

        self.scroll_layout = QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)

        circular_table()
        with sqlite3.connect("employee.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM CIRCULAR")

            rows = cur.fetchall()

        for row in rows:
            year, month, day = row[1].split("-")
            box = CollapsibleBox(f"{row[0]} ({day}-{month}-{year})")
            self.scroll_layout.addWidget(box)
            self.content_layout = QVBoxLayout()
            self.content_layout.addWidget(QLabel(f"{row[2]}"))
            box.setContent(f"{row[2]}")

        self.scroll_area.setWidgetResizable(True)
        self.generalLayout.addWidget(self.scroll_area)


class CircularCtrl:
    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.view = CircularUI()
        self.connectSignals()
        self.set_stylesheet()

    def connectSignals(self) -> None:
        self.view.search_ledit.textChanged.connect(self.search)

        self.view.filter_icon.triggered.connect(self.show_filter)

        self.view.filter_data.ok_btn.clicked.connect(self.filter_data)
        self.view.filter_data.clear_btn.clicked.connect(self.clear_filter)

    def search(self) -> None:
        """
        Searches the circulars for text entered
        """
        with sqlite3.connect("employee.db") as conn:
            cur = conn.cursor()
            cur.execute(
                """SELECT * FROM CIRCULAR
                              WHERE  TITLE          LIKE :query
                                 OR  DESCRIPTION    LIKE :query
                                 OR  CIRCULAR_DATE  LIKE :query""",
                {"query": "%" + self.view.search_ledit.text() + "%"},
            )
            rows = cur.fetchall()

        try:
            self.view.scroll_widget.deleteLater()
        except RuntimeError:
            pass

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        for row in rows:
            year, month, day = row[1].split("-")
            box = CollapsibleBox(f"{row[0]} ({day}-{month}-{year})")
            self.scroll_layout.addWidget(box)
            box.setContent(f"{row[2]}")

        self.scroll_widget.setLayout(self.scroll_layout)
        self.view.scroll_area.setWidget(self.scroll_widget)

    def show_filter(self) -> None:
        """
        Toggles filter's visibilty
        """
        if self.view.filter_data.isVisible():
            self.view.filter_data.hide()
        else:
            self.view.filter_data.show()

    def filter_data(self) -> None:
        """
        Filters according to the date range
        """
        self.date1 = self.view.filter_data.date.date().toPyDate

        self.date2 = self.view.filter_data.date2.date().toPyDate

        with sqlite3.connect("employee.db") as conn:
            cur = conn.cursor()
            cur.execute(
                """SELECT * FROM CIRCULAR
                          WHERE CIRCULAR_DATE BETWEEN ? AND ?""",
                (self.date1(), self.date2()),
            )
            rows = cur.fetchall()

        try:
            self.view.scroll_widget.deleteLater()
        except RuntimeError:
            pass

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        for row in rows:
            year, month, day = row[1].split("-")
            box = CollapsibleBox(f"{row[0]} ({day}-{month}-{year})")
            self.scroll_layout.addWidget(box)
            box.setContent(f"{row[2]}")

        self.scroll_widget.setLayout(self.scroll_layout)
        self.view.scroll_area.setWidget(self.scroll_widget)

    def clear_filter(self) -> None:
        # resetting dates
        self.view.filter_data.date.setDateTime(QDateTime.currentDateTime())
        self.view.filter_data.date2.setDateTime(QDateTime.currentDateTime())

        with sqlite3.connect("employee.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM CIRCULAR")
            rows = cur.fetchall()

        try:
            self.view.scroll_widget.deleteLater()
        except RuntimeError:
            pass

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        for row in rows:
            year, month, day = row[1].split("-")
            box = CollapsibleBox(f"{row[0]} ({day}-{month}-{year})")
            self.scroll_layout.addWidget(box)
            box.setContent(f"{row[2]}")

        self.scroll_widget.setLayout(self.scroll_layout)
        self.view.scroll_area.setWidget(self.scroll_widget)

    def set_stylesheet(self) -> None:
        """ sets the style of widgets according to the stylesheet specified """

        with open("stylesheet.qss", "r") as qss:
            self.app.setStyleSheet(qss.read())

    def run(self) -> int:

        self.view.show()
        return self.app.exec_()


if __name__ == "__main__":
    window = CircularCtrl()
    sys.exit(window.run())
