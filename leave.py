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
        
        self.leaveinfo()
        self.btns()
        self.sub_leave()

    def sub_leave(self):

        self.leave_scroll = QScrollArea()
        self.widget = QWidget()
        self.submitted_leave = QLabel("Submitted Leaves :")
        self.generalLayout.addWidget(self.submitted_leave)
        self.leave_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        #self.leave_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.leave_scroll.setWidgetResizable(True)
        self.leave_scroll.setWidget(self.widget)

        self.generalLayout.addWidget(self.leave_scroll, 2)
        


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
      
        self.reason_label = QLabel("Reason*")

        self.leave_descrip = QTextEdit()

        self.generalLayout.addWidget(self.reason_label)
        self.generalLayout.addWidget(self.leave_descrip)

    def btns(self) -> None:
        """
        Add buttons to add and clear homework
        """
        self.ok = QPushButton()
        self.clear = QPushButton()

        self.ok.setText("Submit")
        self.clear.setText("Clear")

        self.empty = QWidget()
        self.empty.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.empty)
        self.hlayout.addWidget(self.ok)
        self.hlayout.addWidget(self.clear)

        self.generalLayout.addLayout(self.hlayout)


class LeaveCtrl:

    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.view = LeaveUI()
        self.set_stylesheet()
        self.connectSignals()


    def connectSignals(self) -> None:
        """
        Connects signals
        """
        self.view.clear.clicked.connect(self.cancel)

    def cancel(self):
        """
        Clears text in the field
        If button is named "New" connects it to the add function
        """

        self.view.leave_descrip.clear()

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
