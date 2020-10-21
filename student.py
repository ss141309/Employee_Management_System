import sqlite3
import sys

from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtGui import QBrush, QIcon, QTextCharFormat
from PyQt5.QtWidgets import (QApplication, QDateEdit, QFormLayout, QHBoxLayout,
                             QHeaderView, QLabel, QLineEdit, QMainWindow,
                             QPushButton, QScrollArea, QSizePolicy,
                             QStackedWidget, QTableWidget, QTableWidgetItem,
                             QToolButton, QVBoxLayout, QWidget)

from table import student_table


class StudentsUI(QMainWindow):
    def __init__(self, emp_id: str) -> None:
        super().__init__()
        self.emp_id = emp_id
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self.widget = QWidget()
        self.vbox = QVBoxLayout()
        self.widget.setLayout(self.vbox)
        self.generalLayout.addWidget(self.widget)

        self.stacked = QStackedWidget()
        self.stacked.addWidget(self.widget)
        self.generalLayout.addWidget(self.stacked)

        self.get_classes()
        self.search_bar()
        self.btns()
        self.view_students()

    def get_classes(self) -> None:
        """
        Gets classes assigned to the teacher
        """
        with sqlite3.connect("employee.db") as conn:
            cur = conn.cursor()
            cur.execute(
                """SELECT CLASSES_ASSIGNED FROM EMPL
                            WHERE EMP_ID = ?""",
                (self.emp_id,),
            )
            row = cur.fetchone()
            self.row = row[0].split(",")
            self.row = (f'"{x}"' for x in self.row)

    def search_bar(self) -> None:
        """
        Displays a QLineEdit to search students
        """
        self.search_ledit = QLineEdit()
        self.search_ledit.setPlaceholderText("Search")
        self.search_ledit.addAction(
            QIcon("resources/search.svg"), QLineEdit.LeadingPosition
        )
        self.vbox.addWidget(self.search_ledit)

    def view_class_combobox(self) -> None:
        """
        Display all the classes the teacher can select
        """
        pass

    def btns(self) -> None:
        """
        Displays buttons to add and remove students
        """
        self.add_button = QPushButton()
        self.remove_button = QPushButton()

        self.add_button.setIcon(QIcon("resources/plus.svg"))
        self.remove_button.setIcon(QIcon("resources/minus.svg"))

        self.vbox.addWidget(self.add_button)
        self.vbox.addWidget(self.remove_button)

    def view_students(self) -> None:
        """
        View all students in a table
        """
        assigned_classes = (",").join(self.row)
        with sqlite3.connect("employee.db") as conn:
            cur = conn.cursor()
            cur.execute(
                f"""SELECT STUDENT_ID, FIRST_NAME, LAST_NAME, CLASS FROM STUDENT
                                WHERE CLASS IN ({assigned_classes})"""
            )
            rows = cur.fetchall()

        self.student_table = QTableWidget()
        self.student_table.setColumnCount(3)
        self.student_table.setRowCount(len(rows))
        self.student_table.setHorizontalHeaderLabels(
            ["Student ID", "Name", " Class "]
        )
        self.header = self.student_table.horizontalHeader()
        self.header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        for row, value in enumerate(rows):
            std_id = QTableWidgetItem(value[0])
            std_name = QTableWidgetItem(f"{value[1]} {value[2]}")
            std_class = QTableWidgetItem(value[3])

            std_name.setTextAlignment(Qt.AlignCenter)

            # set items not editable
            std_id.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            std_name.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            std_class.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

            self.student_table.setItem(row, 0, std_id)
            self.student_table.setItem(row, 1, std_name)
            self.student_table.setItem(row, 2, std_class)

        self.vbox.addWidget(self.student_table)


class StudentsCtrl:
    def __init__(self, emp_id: str) -> None:
        self.app = QApplication(sys.argv)
        self.view = StudentsUI(emp_id)
        self.connectSignals()
        self.set_stylesheet()

    def connectSignals(self) -> None:
        self.view.search_ledit.textChanged.connect(self.search_student)

    def search_student(self) -> None:
        assigned_classes = (",").join(self.view.row)
        with sqlite3.connect("employee.db") as conn:
            cur = conn.cursor()
            cur.execute(
                f"""SELECT STUDENT_ID, FIRST_NAME, LAST_NAME, CLASS FROM STUDENT
                                                WHERE  (STUDENT_ID   LIKE :query
                                                   OR  FIRST_NAME   LIKE :query
                                                   OR  LAST_NAME    LIKE :query
                                                   OR  CLASS        LIKE :query)
                                                  AND  (CLASS IN ({asssigned_classes})""",
                {"query": "%" + self.view.search_ledit.text() + "%"},
            )
            rows = cur.fetchall()

        self.view.student_table.setRowCount(0)
        self.view.student_table.setRowCount(len(rows))

        for row, value in enumerate(rows):
            std_id = QTableWidgetItem(value[0])
            std_name = QTableWidgetItem(f"{value[1]} {value[2]}")
            std_class = QTableWidgetItem(value[3])

            std_name.setTextAlignment(Qt.AlignCenter)

            # set items not editable
            std_id.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            std_name.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            std_class.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

            self.view.student_table.setItem(row, 0, std_id)
            self.view.student_table.setItem(row, 1, std_name)
            self.view.student_table.setItem(row, 2, std_class)

    def set_stylesheet(self) -> None:
        """ sets the style of widgets according to the stylesheet specified """
        with open("stylesheet.qss", "r") as qss:
            self.app.setStyleSheet(qss.read())

    def run(self) -> int:

        self.view.show()
        return self.app.exec_()


if __name__ == "__main__":
    window = StudentsCtrl("abcd")
    sys.exit(window.run())
