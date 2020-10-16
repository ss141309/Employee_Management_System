# importing libraries
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from icon_win import icon_taskbar

class LeaveUI(QMainWindow):

    def __init__(self) -> None:

        super().__init__()
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        self.form = QFormLayout()
        self.setGeometry(100, 100, 600, 400)
        
        self.leaveinfo()

    def leaveinfo(self):

        self.label = QLabel("From Date*")
        self.label_2 = QLabel("To Date*")

        self.date = QDateEdit(calendarPopup=True)
        self.date.setDateTime(QtCore.QDateTime.currentDateTime())
        self.date2 = QDateEdit(self,calendarPopup=True)
        self.date2.setDateTime(QtCore.QDateTime.currentDateTime())

        self.form.addRow(self.label, self.date)
        self.form.addRow(self.label_2, self.date2)
        self.generalLayout.addLayout(self.form)
      
        self.descrip_label = QLabel("Reason*")

        self.hw_descrip = QTextEdit()

        self.generalLayout.addWidget(self.descrip_label)
        self.generalLayout.addWidget(self.hw_descrip)




class LeaveCtrl:

    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.view = LeaveUI()
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
    window = LeaveCtrl()
    sys.exit(window.run())
