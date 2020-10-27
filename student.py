import sqlite3
import sys

from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtGui import QBrush, QFont, QIcon, QImage, QPixmap, QTextCharFormat
from PyQt5.QtWidgets import (QApplication, QComboBox, QDateEdit, QFormLayout,
                             QGridLayout, QHBoxLayout, QHeaderView, QLabel,
                             QLineEdit, QMainWindow, QMessageBox, QPushButton,
                             QSpinBox, QStackedWidget, QTableWidget,
                             QTableWidgetItem, QVBoxLayout, QWidget)

from overview import InfoCard


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

        self.stacked = QStackedWidget()
        self.stacked.addWidget(self.widget)
        self.generalLayout.addWidget(self.stacked)

        self.get_classes()
        self.search_bar()
        self.btns()
        self.view_students()
        self.add_students()

    def get_classes(self) -> None:
        """
        Gets classes assigned to the teacher
        """
        with sqlite3.connect("employee.db") as conn:
            cur = conn.cursor()
            cur.execute(
                """SELECT CLASSES FROM EMPL
                            WHERE EMP_ID = ?""",
                (self.emp_id,),
            )
            row = cur.fetchone()
            self.row = row[0].split(",")
            self.row = [f'"{x.strip()}"' for x in self.row]

    def search_bar(self) -> None:
        """
        Displays a QLineEdit to search students
        """
        self.hbox = QHBoxLayout()

        self.search_ledit = QLineEdit()
        self.search_ledit.setPlaceholderText("Search")
        self.search_ledit.addAction(
            QIcon("resources/search.svg"), QLineEdit.LeadingPosition
        )
        self.hbox.addWidget(self.search_ledit)
        self.vbox.addLayout(self.hbox)

    def btns(self) -> None:
        """
        Displays buttons to add and remove students
        """
        self.add_button = QPushButton()
        self.remove_button = QPushButton()

        self.add_button.setIcon(QIcon("resources/plus.svg"))
        self.remove_button.setIcon(QIcon("resources/minus.svg"))

        self.hbox.addWidget(self.add_button)
        self.hbox.addWidget(self.remove_button)

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
            self.rows = cur.fetchall()

        self.student_table = QTableWidget()
        self.student_table.setColumnCount(3)
        self.student_table.setRowCount(len(self.rows))
        self.student_table.setHorizontalHeaderLabels(
            ["Student ID", "Name", " Class "]
        )
        self.header = self.student_table.horizontalHeader()
        self.header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        for row, value in enumerate(self.rows):
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

    def add_students(self) -> None:
        """
        Form to add students
        """
        self.add_widget = QWidget()
        self.add_form = QFormLayout()

        self.add_widget.setLayout(self.add_form)
        self.stacked.addWidget(self.add_widget)

        self.add_form.setSpacing(20)

        self.heading = QLabel("Add a Student")
        self.heading.setStyleSheet(
            "QLabel {border: 1px solid white; border-radius: 8px;}"
        )
        self.heading.setFont(QFont("Ariel", 50))

        self.student_id_label = QLabel("Student ID: ")
        self.student_id_ledit = QLineEdit()

        self.first_name_label = QLabel("First Name: ")
        self.first_name_ledit = QLineEdit()

        self.last_name_label = QLabel("Last Name: ")
        self.last_name_ledit = QLineEdit()

        self.gender_label = QLabel("Gender: ")
        self.gender_list = ["Male", "Female"]
        self.gender_combobox = QComboBox()
        self.gender_combobox.addItems(self.gender_list)

        self.dob_label = QLabel("Date of Birth: ")
        self.dob = QDateEdit(calendarPopup=True)
        self.dob.setDateTime(QDateTime.currentDateTime())

        fmt = QTextCharFormat()
        fmt.setForeground(QBrush(Qt.white))

        self.dob.calendarWidget().setWeekdayTextFormat(
            Qt.Saturday, fmt
        )  # setting Saturday white

        self.doj_label = QLabel("Date of Admission: ")
        self.doj = QDateEdit(calendarPopup=True)
        self.doj.setDateTime(QDateTime.currentDateTime())

        self.doj.calendarWidget().setWeekdayTextFormat(
            Qt.Saturday, fmt
        )  # setting Saturday white

        self.class_label = QLabel("Class: ")
        self.class_list = [x.strip('"') for x in self.row]
        self.class_combobox = QComboBox()
        self.class_combobox.addItems(self.class_list)

        self.house_label = QLabel("House: ")
        self.house_list = ["Red", "Green", "Blue", "Yellow"]
        self.house_combobox = QComboBox()
        self.house_combobox.addItems(self.house_list)

        self.rollno_label = QLabel("Roll No.: ")
        self.rollno_spinbox = QSpinBox()

        self.bus_route_label = QLabel("Bus Route: ")
        self.bus_route_ledit = QLineEdit()

        self.email_label = QLabel("Email: ")
        self.email_ledit = QLineEdit()

        self.contact_label = QLabel("Contact: ")
        self.contact_ledit = QLineEdit()

        self.address_label = QLabel("Address: ")
        self.address_ledit = QLineEdit()

        self.add_hbox = QHBoxLayout()
        self.ok_btn = QPushButton()
        self.cancel_btn = QPushButton()
        self.ok_btn.setText("Ok")
        self.cancel_btn.setText("Cancel")
        self.add_hbox.addWidget(QWidget(), 10)
        self.add_hbox.addWidget(self.ok_btn)
        self.add_hbox.addWidget(self.cancel_btn)

        self.add_form.addRow(self.heading)
        self.add_form.addRow(self.student_id_label, self.student_id_ledit)
        self.add_form.addRow(self.first_name_label, self.first_name_ledit)
        self.add_form.addRow(self.last_name_label, self.last_name_ledit)
        self.add_form.addRow(self.gender_label, self.gender_combobox)
        self.add_form.addRow(self.dob_label, self.dob)
        self.add_form.addRow(self.doj_label, self.doj)
        self.add_form.addRow(self.class_label, self.class_combobox)
        self.add_form.addRow(self.house_label, self.house_combobox)
        self.add_form.addRow(self.rollno_label, self.rollno_spinbox)
        self.add_form.addRow(self.bus_route_label, self.bus_route_ledit)
        self.add_form.addRow(self.email_label, self.email_ledit)
        self.add_form.addRow(self.contact_label, self.contact_ledit)
        self.add_form.addRow(self.address_label, self.address_ledit)
        self.add_form.addRow(self.add_hbox)


class StudentsCtrl:
    def __init__(self, emp_id: str) -> None:
        self.app = QApplication(sys.argv)
        self.view = StudentsUI(emp_id)
        self.connectSignals()
        self.set_stylesheet()

    def connectSignals(self) -> None:
        """
        connects signals
        """
        self.view.search_ledit.textChanged.connect(self.search_student)
        self.view.add_button.clicked.connect(
            lambda: self.view.stacked.setCurrentIndex(1)
        )
        self.view.remove_button.clicked.connect(self.remove)
        self.view.ok_btn.clicked.connect(self.add_record)
        self.view.cancel_btn.clicked.connect(self.cancel)

        self.view.student_table.cellDoubleClicked.connect(self.student_info)

    def update_table(self, rows: int) -> None:
        """
        updates table with the new data
        """
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

    def search_student(self) -> None:
        """
        Search data
        """
        assigned_classes = (",").join(self.view.row)
        with sqlite3.connect("employee.db") as conn:
            cur = conn.cursor()
            cur.execute(
                f"""SELECT STUDENT_ID, FIRST_NAME, LAST_NAME, CLASS FROM STUDENT
                                 WHERE CLASS IN ({assigned_classes}) AND
                                      (STUDENT_ID LIKE :query OR
                                       FIRST_NAME LIKE :query OR
                                       LAST_NAME LIKE :query OR
                                       CLASS LIKE :query)""",
                {"query": "%" + self.view.search_ledit.text() + "%"},
            )
            rows = cur.fetchall()
        self.update_table(rows)

    def remove(self) -> None:
        """
        Remove students
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Do you want to delete the selected records?")
        msg.setWindowTitle("Delete Records")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        indexes = self.view.student_table.selectedIndexes()

        returnValue = msg.exec()
        if returnValue == QMessageBox.Ok:
            student_id_list = []
            for index in indexes:
                student_id = self.view.student_table.item(
                    index.row(), 0
                ).text()
                student_id_list.append(f'"{student_id}"')

            assigned_id = (",").join(student_id_list)

            with sqlite3.connect("employee.db") as conn:
                conn.execute(
                    f"delete from student where student_id in ({assigned_id})"
                )

        assigned_classes = (",").join(self.view.row)
        with sqlite3.connect("employee.db") as conn:
            cur = conn.cursor()
            cur.execute(
                f"""SELECT STUDENT_ID, FIRST_NAME, LAST_NAME, CLASS FROM STUDENT
                                WHERE CLASS IN ({assigned_classes})"""
            )
            rows = cur.fetchall()

        self.update_table(rows)

    def add_record(self):
        """
        Add students to database
        """
        dob = self.view.dob.date()
        dob_day = dob.day()
        dob_month = dob.month()
        dob_year = dob.year()

        doj = self.view.doj.date()
        doj_day = doj.day()
        doj_month = doj.month()
        doj_year = doj.year()
        with sqlite3.connect("employee.db") as conn:
            conn.execute(
                "INSERT INTO STUDENT VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    self.view.student_id_ledit.text(),
                    self.view.first_name_ledit.text(),
                    self.view.last_name_ledit.text(),
                    self.view.gender_combobox.currentText(),
                    f"{dob_day}-{dob_month}-{dob_year}",
                    f"{doj_day}-{doj_month}-{doj_year}",
                    self.view.class_combobox.currentText(),
                    self.view.house_combobox.currentText(),
                    self.view.rollno_spinbox.text(),
                    self.view.bus_route_ledit.text(),
                    self.view.email_ledit.text(),
                    self.view.contact_ledit.text(),
                    self.view.address_ledit.text(),
                ),
            )

        assigned_classes = (",").join(self.view.row)
        with sqlite3.connect("employee.db") as conn:
            cur = conn.cursor()
            cur.execute(
                f"""SELECT STUDENT_ID, FIRST_NAME, LAST_NAME, CLASS FROM STUDENT
                                WHERE CLASS IN ({assigned_classes})"""
            )
            rows = cur.fetchall()

        self.update_table(rows)

        self.view.stacked.setCurrentIndex(0)

    def cancel(self):
        """
        go back to view students
        """
        self.view.stacked.setCurrentIndex(0)

        self.view.student_id_ledit.clear()
        self.view.first_name_ledit.clear()
        self.view.last_name_ledit.clear()
        self.view.dob.setDateTime(QDateTime.currentDateTime())
        self.view.doj.setDateTime(QDateTime.currentDateTime())
        self.view.rollno_spinbox.clear()
        self.view.email_ledit.clear()
        self.view.contact_ledit.clear()
        self.view.address_ledit.clear()

    def student_info(self):
        """
        view student information
        """
        row = self.view.student_table.currentRow()

        with sqlite3.connect("employee.db") as conn:
            cur = conn.cursor()

            cur.execute(
                "select * from student where student_id = ?",
                (self.view.student_table.item(row, 0).text(),),
            )
            (
                student_id,
                first_name,
                last_name,
                gender,
                dob,
                doj,
                student_class,
                house,
                rollno,
                bus_route,
                email,
                contact,
                address,
            ) = cur.fetchone()

        info_widget = QWidget()
        general_grid = QGridLayout()
        info_grid = QGridLayout()
        info_widget.setLayout(general_grid)
        self.view.stacked.addWidget(info_widget)

        frame = QWidget()
        label_Image = QLabel(frame)

        image_path = "resources/konqi-alt.png"
        image_profile = QImage(image_path)
        image_profile = image_profile.scaled(
            250,
            250,
            aspectRatioMode=Qt.KeepAspectRatio,
            transformMode=Qt.SmoothTransformation,
        )  # To scale image and keep its Aspect Ratio

        label_Image.setPixmap(QPixmap.fromImage(image_profile))

        info_label = QLabel("Student Information")
        info_label.setFont(QFont("Ariel", 50))

        self.id_card = InfoCard(
            "resources/id-card-alt.svg", "Student ID", student_id
        )
        info_grid.addWidget(self.id_card, 0, 0)

        self.name_card = InfoCard(
            "resources/user.svg", "Name", f"{first_name} {last_name}"
        )
        info_grid.addWidget(self.name_card, 0, 1)

        self.gender_card = InfoCard(
            "resources/venus-mars.svg", "Gender", gender
        )
        info_grid.addWidget(self.gender_card, 0, 2)

        self.dob_card = InfoCard(
            "resources/calendar-day.svg", "Date of Birth", dob
        )
        info_grid.addWidget(self.dob_card, 1, 0)

        self.doj_card = InfoCard(
            "resources/calendar-alt.svg", "Admisson Date", doj
        )
        info_grid.addWidget(self.doj_card, 1, 1)

        self.class_card = InfoCard(
            "resources/chalkboard.svg", "Class", student_class
        )
        info_grid.addWidget(self.class_card, 1, 2)

        self.house_card = InfoCard("resources/house-user.svg", "House", house)
        info_grid.addWidget(self.house_card, 2, 0)

        self.rollno_card = InfoCard(
            "resources/id-card.svg", "Roll No", str(rollno)
        )
        info_grid.addWidget(self.rollno_card, 2, 1)

        self.bus_route_card = InfoCard(
            "resources/bus-alt.svg", "Bus Route", bus_route
        )
        info_grid.addWidget(self.bus_route_card, 2, 2)

        self.email_card = InfoCard("resources/envelope.svg", "Email", email)
        info_grid.addWidget(self.email_card, 3, 0)

        self.contact_card = InfoCard(
            "resources/mobile-alt.svg", "Contact", contact
        )
        info_grid.addWidget(self.contact_card, 3, 1)

        self.address_card = InfoCard(
            "resources/address-book.svg", "Address", address
        )
        info_grid.addWidget(self.address_card, 3, 2)

        ok_btn = QPushButton()
        ok_btn.setText("Ok")
        ok_btn.clicked.connect(
            lambda: [
                self.view.stacked.setCurrentIndex(0),
                info_widget.deleteLater(),
            ]
        )

        general_grid.addWidget(label_Image, 0, 0)
        general_grid.addWidget(info_label, 0, 1)
        general_grid.addLayout(info_grid, 1, 0, 5, 5)
        general_grid.addWidget(ok_btn, 6, 4)

        self.view.stacked.setCurrentIndex(2)

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
