import os.path

from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton


class FileItem(QWidget):
    def __init__(self, parent, file_url: str):
        super().__init__(parent)
        self.file_url = file_url
        self.onRemove = lambda _: None
        filename = os.path.split(file_url)[1]
        self.label = QLabel(parent=self)
        self.label.setGeometry(QtCore.QRect(0, 0, 580, 30))
        self.label.setText(filename)
        self.label.setStyleSheet("background-color: #ddd; padding-left: 10px; border-radius: 5px")
        self.label_progress = QLabel(parent=self)
        self.label_progress.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.label_progress.setText(filename)
        self.label_progress.setStyleSheet("background-color: #ccc; padding-left: 10px; border-radius: 5px")
        self.label_state = QLabel(parent=self)
        self.label_state.setGeometry(QtCore.QRect(480, 5, 60, 20))
        self.label_state.setText('')
        self.label_state.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.button = QPushButton(parent=self)
        self.button.setGeometry(QtCore.QRect(550, 0, 30, 30))
        self.button.setText('X')
        self.button.clicked.connect(lambda: self.onRemove(file_url))
        self.state = 0
        self.set_state(0)

    def set_progress(self, percent: int):
        self.label_progress.setGeometry(QtCore.QRect(0, 0, int(percent * 5.8), 30))

    def set_state(self, value: int):
        self.state = value
        self.label_state.show()
        if value == 0:
            self.label_state.hide()
        elif value == 1:
            self.label_state.setText('待处理')
            self.label_state.setStyleSheet("background-color: #bbb; border-radius: 5px")
        elif value == 2:
            self.label_state.setText('生成中')
            self.label_state.setStyleSheet("background-color: #bbb; border-radius: 5px")
        elif value == 3:
            self.label_state.setText('已完成')
            self.label_state.setStyleSheet("background-color: #bbb; border-radius: 5px")
        elif value == 4:
            self.label_state.setText('解析失败')
            self.label_state.setStyleSheet("background-color: #bbb; border-radius: 5px")

    def deleteLater(self):
        self.label.deleteLater()
        self.label_progress.deleteLater()
        self.button.deleteLater()
        super().deleteLater()
