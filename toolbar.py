#! /usr/bin/env python3

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QActionGroup, QSizePolicy, QToolBar,
                             QWidget, QMainWindow)



class ToolBar(QMainWindow):
    """
    Sets up the ToolBar
    """

    def __init__(self) -> None:
        super().__init__()
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
