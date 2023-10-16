from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QFileDialog

from ui.FileItem import FileItem
from ui.Form3 import Form3
from ui.Ui_Form2 import Ui_Form2


class Form2(QWidget, Ui_Form2):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.files = set()
        self.file_items: list[FileItem] = list()
        self.setup()
        self.frame_list.hide()
        self.frame_upload.hide()

    def setup(self):
        self.setupUi(self)
        self.pushButton_cancel.clicked.connect(lambda: self.close())
        self.pushButton_next.clicked.connect(self._next)
        self.label_drops.mousePressEvent = self._upload
        self.pushButton_upload.clicked.connect(self._upload)

    def dragEnterEvent(self, a0):
        a0.accept()

    def dropEvent(self, a0):
        self._add(a0.mimeData().text().split('\n'))

    def _upload(self, _):
        files = QFileDialog.getOpenFileUrls(self, '选择文件', filter="文件格式(*.pdf;*.doc;*.docx)")[0]
        self._add([qurl.url() for qurl in files])

    def _add(self, file_urls: list[str]):
        for file_url in file_urls:
            if not file_url.startswith('file://'):
                continue
            if not file_url.endswith('.doc') and not file_url.endswith('.docx') and not file_url.endswith('.pdf'):
                continue
            if file_url not in self.files:
                item = FileItem(self.frame_list, file_url)
                item.onRemove = self._delete
                item.show()
                self.file_items.append(item)
                self.files.add(file_url)
        self._render_list()

    def _delete(self, filepath: str):
        index = -1
        for i, item in enumerate(self.file_items):
            if item.file_url == filepath:
                item.deleteLater()
                index = i
                break
        self.file_items.pop(index)
        self.files.remove(filepath)
        self._render_list()

    def _render_list(self):
        for item in self.file_items[10:]:
            item.deleteLater()
            self.files.remove(item.file_url)
        self.file_items = self.file_items[:10]
        count = len(self.file_items)
        for i, item in enumerate(self.file_items):
            item.setGeometry(QtCore.QRect(0, i * 35, 580, 30))
        self.frame_upload.setGeometry(QtCore.QRect(
            40, count * 35 + 40,
            self.frame_upload.width(),
            self.frame_upload.height(),
        ))
        if count:
            self.label_drops.hide()
            self.frame_list.show()
            self.frame_upload.show()
        else:
            self.label_drops.show()
            self.frame_list.hide()
            self.frame_upload.hide()

    def _next(self):
        file_urls = [item.file_url for item in self.file_items]
        next_window = Form3(file_urls=file_urls)
        next_window.show()
        self.close()
