import sqlite3
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from table import circular_table


class CollapsibleBox(QWidget):
    def __init__(self, title: str = "") -> None:
        super(CollapsibleBox, self).__init__()

        self.toggle_button = QToolButton(
            text=title, checkable=True, checked=False
        )
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(Qt.RightArrow)
        self.toggle_button.pressed.connect(self.on_pressed)

        self.toggle_animation = QParallelAnimationGroup(self)

        self.content_area = QScrollArea(maximumHeight=0, minimumHeight=0)
        self.content_area.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed
        )
        self.content_area.setFrameShape(QFrame.NoFrame)

        lay = QVBoxLayout(self)
        # lay.setSpacing(0)
        # lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.toggle_button)
        lay.addWidget(self.content_area)

        self.toggle_animation.addAnimation(
            QPropertyAnimation(self, b"minimumHeight")
        )
        self.toggle_animation.addAnimation(
            QPropertyAnimation(self, b"maximumHeight")
        )
        self.toggle_animation.addAnimation(
            QPropertyAnimation(self.content_area, b"maximumHeight")
        )

    @pyqtSlot()
    def on_pressed(self) -> None:
        checked = self.toggle_button.isChecked()
        self.toggle_button.setArrowType(
            Qt.DownArrow if not checked else Qt.RightArrow
        )
        self.toggle_animation.setDirection(
            QAbstractAnimation.Forward
            if not checked
            else QAbstractAnimation.Backward
        )
        self.toggle_animation.start()

    def setContentLayout(self, layout) -> None:
        lay = self.content_area.layout()
        del lay
        self.content_area.setLayout(layout)
        collapsed_height = (
            self.sizeHint().height() - self.content_area.maximumHeight()
        )
        content_height = layout.sizeHint().height()
        for i in range(self.toggle_animation.animationCount()):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(500)
            animation.setStartValue(collapsed_height)
            animation.setEndValue(collapsed_height + content_height)

        content_animation = self.toggle_animation.animationAt(
            self.toggle_animation.animationCount() - 1
        )
        content_animation.setDuration(500)
        content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)


class CircularUI(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self.search_bar()
        self.collapsible_circular()

    def search_bar(self) -> None:
        self.search_ledit = QLineEdit()
        self.search_ledit.setPlaceholderText("Search")
        self.search_ledit.addAction(
            QIcon("resources/search.svg"), QLineEdit.LeadingPosition
        )

        self.generalLayout.addWidget(self.search_ledit)

    def collapsible_circular(self) -> None:
        self.scroll_area = QScrollArea()

        self.scroll_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_widget)

        self.scroll_layout = QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)

        circular_table()
        with sqlite3.connect("employee.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM CIRCULAR")

            rows = cur.fetchall()

        for row in rows:
            box = CollapsibleBox(f"{row[0]} ({row[1]}-{row[2]}-{row[3]})")
            self.scroll_layout.addWidget(box)
            self.content_layout = QVBoxLayout()
            self.content_layout.addWidget(QLabel(f"{row[4]}"))
            box.setContentLayout(self.content_layout)

        self.scroll_area.setWidgetResizable(True)
        self.generalLayout.addWidget(self.scroll_area)


class CircularCtrl:
    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.view = CircularUI()
        self.connectSignals()
        self.set_stylesheet()

    def connectSignals(self) -> None:
        self.view.search_ledit.textChanged.connect(self.search)

    def search(self) -> None:
        with sqlite3.connect("employee.db") as conn:
            cur = conn.cursor()
            cur.execute(
                """SELECT * FROM CIRCULAR
                              WHERE TITLE LIKE :query
                                OR  DESCRIPTION LIKE :query""",
                {"query": "%" + self.view.search_ledit.text() + "%"},
            )
            rows = cur.fetchall()

        try:
            self.view.scroll_widget.deleteLater()
        except RuntimeError:
            pass

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        for row in rows:
            box = CollapsibleBox(f"{row[0]} ({row[1]}-{row[2]}-{row[3]})")
            self.scroll_layout.addWidget(box)
            self.content_layout = QVBoxLayout()
            self.content_layout.addWidget(QLabel(f"{row[4]}"))
            box.setContentLayout(self.content_layout)

        self.scroll_widget.setLayout(self.scroll_layout)
        self.view.scroll_area.setWidget(self.scroll_widget)

    def set_stylesheet(self) -> None:
        """ sets the style of widgets according to the stylesheet specified """

        with open("stylesheet.qss", "r") as qss:
            self.app.setStyleSheet(qss.read())

    def run(self) -> int:

        self.view.show()
        return self.app.exec_()


if __name__ == "__main__":
    window = CircularCtrl()
    sys.exit(window.run())
