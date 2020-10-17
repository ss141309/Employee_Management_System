import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class CollapsibleBox(QWidget):
    def __init__(self, title="", parent=None):
        super(CollapsibleBox, self).__init__(parent)

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
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)
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
    def on_pressed(self):
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

    def setContentLayout(self, layout):
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
    def __init__(self):
        super().__init__()
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self.collapsible_circular()

    def collapsible_circular(self):
        self.scroll_area = QScrollArea()

        self.scroll_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_widget)

        self.scroll_layout = QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)

        for i in range(10):
            box = CollapsibleBox(str(i))
            self.scroll_layout.addWidget(box)
            self.content_layout = QVBoxLayout()
            for j in range(8):
                label = QLabel("Hello")
                self.content_layout.addWidget(label)
            box.setContentLayout(self.content_layout)

        self.scroll_area.setWidgetResizable(True)
        self.generalLayout.addWidget(self.scroll_area)


class CircularCtrl:
    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.view = CircularUI()
        self.set_stylesheet()

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


# if __name__ == "__main__":
#     import random
#     import sys

#     app = QtWidgets.QApplication(sys.argv)

#     w = QtWidgets.QMainWindow()
#     center = QtWidgets.QWidget()
#     w.setCentralWidget(center)
#     vbox = QtWidgets.QVBoxLayout()
#     center.setLayout(vbox)
#     scroll = QtWidgets.QScrollArea()
#     vbox.addWidget(scroll)
#     content = QtWidgets.QWidget()
#     scroll.setWidget(content)
#     scroll.setWidgetResizable(True)
#     vlay = QtWidgets.QVBoxLayout(content)
#     for i in range(10):
#         box = CollapsibleBox(str(i))
#         vlay.addWidget(box)
#         lay = QtWidgets.QVBoxLayout()
#         for j in range(8):
#             label = QtWidgets.QLabel("Hello")
#             label.setAlignment(QtCore.Qt.AlignCenter)
#             lay.addWidget(label)

#         box.setContentLayout(lay)
#     vlay.addStretch()
#     w.resize(640, 480)
#     w.show()
#     sys.exit(app.exec_())
