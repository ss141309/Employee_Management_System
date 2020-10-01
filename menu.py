#! /usr/bin/env python3
import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QActionGroup, QApplication, QMainWindow,
                             QSizePolicy, QSpacerItem, QToolBar, QVBoxLayout,
                             QWidget)

from icon_win import icon_taskbar


class MainUI(QMainWindow):
    """
    Sets up the UI of the Main Window
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowIcon(QIcon("resources/icon.svg"))
        self.setWindowTitle("Main Menu")
        self.setGeometry(100, 100, 1200, 750)

        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self.top_bar()

    def top_bar(self) -> None:
        self.toolbar = QToolBar("My Main Toolbar")
        self.toolbar.setIconSize(QSize(100, 100))
        self.toolbar.setFixedHeight(128)

        self.dashboard_btn = QAction(QIcon("resources/house-user.svg"), "Overview", self)
        self.student_btn = QAction(QIcon("resources/id-card-alt.svg"), "Students", self)
        self.attendance_btn = QAction(QIcon("resources/calendar-alt.svg"), "Attendance", self)
        self.homework_btn = QAction(QIcon("resources/book.svg"), "Homework", self)
        self.circular_btn = QAction(QIcon("resources/newspaper.svg"), "Circular", self)
        self.medical_btn = QAction(QIcon("resources/receipt.svg"), "Apply Leave", self)

        self.group = QActionGroup(self)
        self.group.setExclusive(True)

        # creates empty widgets to set up space between the toolbar icons
        self.empty_widget_list = []
        for i in range(5):
            empty_widget = QWidget()
            empty_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            self.empty_widget_list.append(empty_widget)

        # sets the toolbar icons checkable
        self.checkable_btns_list = []
        for checkable_btns in (self.dashboard_btn, self.student_btn, self.attendance_btn, self.homework_btn, self.circular_btn, self.medical_btn):
            checkable_btns.setCheckable(True)
            self.checkable_btns_list.append(checkable_btns)

        # adds the toolbar icons and empty space to the toolbar
        # also sets up the condition that only one icon at a
        # time can be checkable
        for tool_btn in range(6):
            try:
                self.toolbar.addAction(self.checkable_btns_list[tool_btn])
                self.group.addAction(self.checkable_btns_list[tool_btn])
                self.toolbar.addWidget(self.empty_widget_list[tool_btn])
            except IndexError:
                break
            
        self.toolbar.addSeparator()
        self.toolbar.setMovable(False)
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.addToolBar(self.toolbar)


class MainCtrl:
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
