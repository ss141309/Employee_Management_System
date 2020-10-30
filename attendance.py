import sqlite3
import sys
from typing import Tuple

from PyQt5.QtChart import (QBarCategoryAxis, QBarSeries, QBarSet, QChart,
                           QChartView, QPieSeries, QPieSlice, QValueAxis)
from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtGui import QBrush, QFont, QIcon, QImage, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import (QApplication, QGridLayout, QHBoxLayout,
                             QHeaderView, QLabel, QLineEdit, QMainWindow,
                             QPushButton, QSizePolicy, QStackedWidget,
                             QTableWidget, QTableWidgetItem, QVBoxLayout,
                             QWidget)


class AttendanceUI(QMainWindow):
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
        self.view_students()
        

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
        
    def view_students(self):
        """
        View all students in a table
        """
        assigned_classes = (",").join(self.row)
        with sqlite3.connect("employee.db") as conn:
            cur = conn.cursor()
            cur.execute(
                f"""SELECT STUDENT_ID, FIRST_NAME, LAST_NAME, CLASS , DAYS_PRESENT, TOTAL_WORKING_DAYS FROM STUDENT
                                WHERE CLASS IN ({assigned_classes})"""
            )
            self.rows = cur.fetchall()

        self.student_table = QTableWidget()
        self.student_table.setColumnCount(5)
        self.student_table.setRowCount(len(self.rows))
        self.student_table.setHorizontalHeaderLabels(
            ["Student ID", "Name", " Class ", "Attendance Percentage", "Days Present/Total Working Days"]
        )
        self.header = self.student_table.horizontalHeader()
        self.header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        for row, value in enumerate(self.rows):
            std_id = QTableWidgetItem(value[0])
            std_name = QTableWidgetItem(f"{value[1]} {value[2]}")
            std_class = QTableWidgetItem(value[3])
            std_percentage = QTableWidgetItem(f"{round((value[4]*100)/value[5],2)}")
            std_ratio = QTableWidgetItem(f"{value[4]}/{value[5]}")

            std_name.setTextAlignment(Qt.AlignCenter)
            std_percentage.setTextAlignment(Qt.AlignCenter)
            std_ratio.setTextAlignment(Qt.AlignCenter)

            # set items not editable
            std_id.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            std_name.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            std_class.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            std_percentage.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            std_ratio.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

            self.student_table.setItem(row, 0, std_id)
            self.student_table.setItem(row, 1, std_name)
            self.student_table.setItem(row, 2, std_class)
            self.student_table.setItem(row, 3, std_percentage)
            self.student_table.setItem(row, 4, std_ratio)

            self.vbox.addWidget(self.student_table)


class AttendanceCtrl:
    def __init__(self, emp_id: str) -> None:
        self.app = QApplication(sys.argv)
        self.view = AttendanceUI(emp_id)
        self.connectSignals()
        self.set_stylesheet()

    def connectSignals(self) -> None:

        self.view.search_ledit.textChanged.connect(self.search_student)
        self.view.student_table.cellDoubleClicked.connect(self.graphs)

    def update_table(self, rows: int) -> None:
        """
        updates table with the new data
        """
        self.view.student_table.setRowCount(len(rows))
        for row, value in enumerate(rows):
            std_id = QTableWidgetItem(value[0])
            std_name = QTableWidgetItem(f"{value[1]} {value[2]}")
            std_class = QTableWidgetItem(value[3])
            std_percentage = QTableWidgetItem(f"{round((value[4]*100)/value[5],2)}")
            std_ratio = QTableWidgetItem(f"{value[4]}/{value[5]}")

            std_name.setTextAlignment(Qt.AlignCenter)
            std_percentage.setTextAlignment(Qt.AlignCenter)
            std_ratio.setTextAlignment(Qt.AlignCenter)

            # set items not editable
            std_id.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            std_name.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            std_class.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            std_percentage.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            std_ratio.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

            self.view.student_table.setItem(row, 0, std_id)
            self.view.student_table.setItem(row, 1, std_name)
            self.view.student_table.setItem(row, 2, std_class)
            self.view.student_table.setItem(row, 3, std_percentage)
            self.view.student_table.setItem(row, 4, std_ratio)

    def search_student(self) -> None:
        """
        Search data
        """
        assigned_classes = (",").join(self.view.row)
        with sqlite3.connect("employee.db") as conn:
            cur = conn.cursor()
            cur.execute(
                f"""SELECT STUDENT_ID, FIRST_NAME, LAST_NAME, CLASS, DAYS_PRESENT, TOTAL_WORKING_DAYS FROM STUDENT
                                 WHERE CLASS IN ({assigned_classes}) AND
                                      (STUDENT_ID LIKE :query OR
                                       FIRST_NAME LIKE :query OR
                                       LAST_NAME LIKE :query OR
                                       CLASS LIKE :query OR
                                       DAYS_PRESENT LIKE :query OR
                                       TOTAL_WORKING_DAYS LIKE :query)""",
                {"query": "%" + self.view.search_ledit.text() + "%"},
            )
            rows = cur.fetchall()
        self.update_table(rows)

    def graphs(self) -> None:
        widget = QWidget()
        grid_layout = QGridLayout()
        widget.setLayout(grid_layout)

        row = self.view.student_table.currentRow()

        with sqlite3.connect("employee.db") as conn:
            cur = conn.cursor()
            cur.execute(
                f"""SELECT DAYS_JAN, DAYS_FEB, DAYS_MAR, DAYS_APR, DAYS_MAY , DAYS_JUN, DAYS_JUL, DAYS_AUG, DAYS_SEPT, DAYS_OCT, DAYS_NOV, DAYS_DEC, DAYS_PRESENT, TOTAL_WORKING_DAYS
                    FROM STUDENT WHERE STUDENT_ID = ?""", (self.view.student_table.item(row, 0).text(),)
            )
            self.row = cur.fetchone()
            
            bar_graph = self.bargraph(self.row[0:12])
            pie_chart = self.pie_chart(self.row[12:])
            btn = QPushButton()
            btn.setText("Ok")

            btn.clicked.connect(lambda: [self.view.stacked.setCurrentIndex(0), bar_graph.deleteLater(), pie_chart.deleteLater()])
            

            grid_layout.addWidget(bar_graph,0,0 )
            grid_layout.addWidget(pie_chart, 0, 1)
            grid_layout.addWidget(btn, 2, 0,2,2)
            self.view.stacked.addWidget(widget)
            self.view.stacked.setCurrentIndex(1)


    def bargraph(self, rows: Tuple[int]) -> None:
    
        widget = QWidget()
        vbox = QVBoxLayout()
        widget.setLayout(vbox)


        set1 = QBarSet('Days Present')
        set2 = QBarSet('Total Working Days')
        
        set1.append([rows[0],rows[1],rows[2],rows[3],rows[4],rows[5],rows[6],rows[7],rows[8],rows[9],rows[10],rows[11]])
        set2.append([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
        series = QBarSeries()
        series.append(set1)
        series.append(set2)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle('Monthly Attendace')
        chart.setAnimationOptions(QChart.SeriesAnimations)

        months = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec')

        axisX = QBarCategoryAxis()
        axisX.append(months)

        axisY = QValueAxis()
        axisY.setRange(1, 31)

        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        self.chartView = QChartView(chart)

        return self.chartView

    def pie_chart(self, row):

        series = QPieSeries()
        series.append("Days Present", row[0])
        series.append("Total Working Days", row[1])
        
        slice = QPieSlice()
        slice = series.slices()[1]
        slice.setExploded(False)
        slice.setLabelVisible(True)
        slice.setPen(QPen(Qt.darkGreen, 2))
        slice.setBrush(Qt.green)

        chart = QChart()
        chart.legend().hide()
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Attendance Overiew")

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)

        return chartview


    def set_stylesheet(self) -> None:
        """ sets the style of widgets according to the stylesheet specified """
        with open("stylesheet.qss", "r") as qss:
            self.app.setStyleSheet(qss.read())

    def run(self) -> int:

        self.view.show()
        return self.app.exec_()

if __name__ == "__main__":
    window = AttendanceCtrl("abcd")
    sys.exit(window.run())
