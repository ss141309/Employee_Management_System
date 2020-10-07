#! /usr/bin/env python3
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QStackedLayout,
                             QVBoxLayout, QWidget)

from hw import HomeWorkCtrl
from icon_win import icon_taskbar
from leave import LeaveCtrl
from toolbar import ToolBar


class MainUI(QMainWindow):
    """
    Sets up the UI of the Main Window
    """

    def __init__(self) -> None:
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

        self.hw = HomeWorkCtrl()
        self.generalLayout.addWidget(self.hw.view._centralWidget)

        self.leave = LeaveCtrl()
        self.generalLayout.addWidget(self.leave.view._centralWidget)

#        self.generalLayout.setCurrentIndex(2)
        
   
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

