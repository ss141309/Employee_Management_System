#! /usr/bin/env python3
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QToolBar, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt

from icon_win import icon_taskbar

class MainUI(QMainWindow):
    """
    Sets up the UI of the Main Window
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowIcon(QIcon("resources/icon.svg"))
        self.setWindowTitle("Main Menu")
        self.setGeometry(100,100, 1200, 750)

        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self.top_bar()

    def top_bar(self):
        self.toolbar = QToolBar("My main toolbar")
        self.toolbar.setIconSize(QSize(100, 100))
        self.toolbar.setFixedHeight(128)

        self.dashboard_btn = QAction(QIcon("resources/house-user.svg"), "Dashboard", self)
        self.student_btn = QAction(QIcon("resources/id-card-alt.svg"), "Students", self)
        self.attendance_btn = QAction(QIcon("resources/calendar-alt.svg"), "Attendance", self)
        
        self.toolbar.addAction(self.dashboard_btn)
        self.toolbar.addAction(self.student_btn)
        self.toolbar.addAction(self.attendance_btn)
        
        self.toolbar.addSeparator()
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.addToolBar(self.toolbar)


class MainCtrl():
    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.view = MainUI()
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
