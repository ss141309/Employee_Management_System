import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from icon_win import icon_taskbar

class MainUI(QDialog):

    """ Sets up the UI of the Main Window"""

    def __init__(self) -> None:


        super().__init__()
        self.setWindowIcon(QIcon("resources/icon.svg"))
        self.setWindowTitle("Main Menu")
        self.setGeometry(100,100, 1200, 750)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

        self.generalLayout = QGridLayout()
        self.setLayout(self.generalLayout)

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
