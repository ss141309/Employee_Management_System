#! /usr/bin/env python3
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedLayout, QWidget

from circular import CircularCtrl
from hw import HomeWorkCtrl
from icon_win import icon_taskbar
from leave import LeaveCtrl
from overview import DashBoardCtrl
from student import StudentsCtrl
from toolbar import ToolBar


class MainUI(QMainWindow):
    """
    Sets up the UI of the Main Window
    """
    def __init__(self, emp_id: str) -> None:
        super().__init__()
        self.setWindowIcon(QIcon("resources/icon.svg"))
        self.setWindowTitle("Main Menu")
        self.setGeometry(100, 100, 1200, 750)

        self.generalLayout = QStackedLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self.tool_bar = ToolBar()
        self.addToolBar(self.tool_bar.toolbar)

        self.ovrvw = DashBoardCtrl(emp_id)
        self.generalLayout.addWidget(self.ovrvw.view._centralWidget)

        self.student = StudentsCtrl(emp_id)
        self.generalLayout.addWidget(self.student.view._centralWidget)

        self.hw = HomeWorkCtrl(emp_id)
        self.generalLayout.addWidget(self.hw.view._centralWidget)

        self.circular = CircularCtrl()
        self.generalLayout.addWidget(self.circular.view._centralWidget)

        self.leave = LeaveCtrl(emp_id)
        self.generalLayout.addWidget(self.leave.view._centralWidget)

        
        self.connect_toolbar()

    def connect_toolbar(self) -> None:
        """
        opens the correct page for each button clicked
        """
        self.tool_bar.dashboard_btn.triggered.connect(lambda: self.generalLayout.setCurrentIndex(0))
        self.tool_bar.student_btn.triggered.connect(lambda: self.generalLayout.setCurrentIndex(1))
        self.tool_bar.homework_btn.triggered.connect(lambda: self.generalLayout.setCurrentIndex(2))
        self.tool_bar.circular_btn.triggered.connect(lambda: self.generalLayout.setCurrentIndex(3))        
        self.tool_bar.medical_btn.triggered.connect(lambda: self.generalLayout.setCurrentIndex(4))


class MainCtrl:
    def __init__(self,  emp_id: str = "abcd") -> None:
        self.app = QApplication(sys.argv)
        self.view = MainUI(emp_id)
        self.set_stylesheet()

    def set_stylesheet(self) -> None:
        """ sets the style of widgets according to the stylesheet specified """

        with open("stylesheet.qss", "r") as qss:
            self.app.setStyleSheet(qss.read())

    def run(self) -> int:

        self.view.show()
        return self.app.exec_()


if __name__ == "__main__":
    icon_taskbar()
    window = MainCtrl()
    sys.exit(window.run())
