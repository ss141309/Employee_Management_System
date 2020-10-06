#! /usr/bin/env python3
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QLabel,
    QComboBox,
    QTextEdit,
)

from icon_win import icon_taskbar


class HomeWorkUI(QMainWindow):
    """
    Sets up the UI of the HomeWork option
    """

    def __init__(self) -> None:
        super().__init__()
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self.title()
        self.student_class()
        self.descrip()

    def title(self) -> None:
        self.title_label = QLabel("Title")
        self.title_ledit = QLineEdit()

        self.generalLayout.addWidget(self.title_label)
        self.generalLayout.addWidget(self.title_ledit)

    def student_class(self) -> None:
        self.class_label = QLabel("Class")
        class_list = (
            "Pre Nursery",
            "Nursery",
            "KG",
            "I",
            "II",
            "III",
            "IV",
            "V",
            "VI",
            "VII",
            "VIII",
            "IX",
            "X",
            "XI",
            "XII",
        )

        self.combo_box = QComboBox()
        self.combo_box.addItems(class_list)
        self.combo_box.setGeometry(200, 150, 150, 30)
        self.generalLayout.addWidget(self.class_label)
        self.generalLayout.addWidget(self.combo_box)

    def descrip(self):
        self.descrip_label = QLabel("Description")
        self.descrip = QTextEdit()
        self.generalLayout.addWidget(self.descrip_label)
        self.generalLayout.addWidget(self.descrip)


class HomeWorkCtrl:
    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.view = HomeWorkUI()
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
