from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget

from ui.FileItem import FileItem
from ui.Ui_Form3 import Ui_Form3


class Form3(QWidget, Ui_Form3):
    def __init__(self, parent=None, file_urls: list[str] = None):
        super().__init__(parent=parent)
        self.file_urls = file_urls if file_urls else []
        self.file_items: list[FileItem] = list()
        self.setup()

    def setup(self):
        self.setupUi(self)
        self.pushButton_cancel.clicked.connect(lambda: self.close())

        for file_url in self.file_urls:
            item = FileItem(self.frame_list, file_url)
            item.onRemove = self._delete
            item.set_state(1)
            self.file_items.append(item)
        self._render_list()

    def _delete(self, filepath: str):
        index = -1
        for i, item in enumerate(self.file_items):
            if item.file_url == filepath:
                item.deleteLater()
                index = i
                break
        self.file_items.pop(index)
        self._render_list()

    def _render_list(self):
        for item in self.file_items[10:]:
            item.deleteLater()
        self.file_items = self.file_items[:10]
        for i, item in enumerate(self.file_items):
            item.setGeometry(QtCore.QRect(0, i * 35, 580, 30))
        self._render_count()

    def _render_count(self):
        count = len([None for item in self.file_items if item.state in (1, 2)])
        self.label_hint.setText(f'{count} 个文档正在生成问答对')
