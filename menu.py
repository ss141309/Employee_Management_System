from PyQt5.QtWidgets import *
import ctypes
import sys
from PyQt5.QtGui import QIcon, QImage, QPixmap, QFont
from PyQt5.QtCore import Qt

def icon_taskbar() -> None:
    """
    Tells windows,that the program running is using Python as a host,
    so that its taskbar icon can be displayed, see: https://bit.ly/3fv9kr7
    """

    if sys.platform == "win32":
        myappid = "abcd"  # arbitrary string

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

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
