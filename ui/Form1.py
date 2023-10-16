import json
from urllib import request, parse, error

from PyQt6.QtWidgets import QWidget, QMessageBox

from ui.Form2 import Form2
from ui.Ui_Form1 import Ui_Form1


class Form1(QWidget, Ui_Form1):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setup()

    def setup(self):
        self.setupUi(self)
        self.checkBox_proxy.stateChanged.connect(
            lambda v: self.widget_proxy.setEnabled(bool(v))
        )
        self.pushButton_test.clicked.connect(self._test)
        self.pushButton_next.clicked.connect(self._next)

    @property
    def data(self) -> dict[str, str]:
        proxy_pass = self.lineEdit_proxy_pass.text()
        if not proxy_pass:
            proxy_pass = self.lineEdit_proxy_pass.placeholderText()
        return dict(
            apikey=self.lineEdit_apikey.text(),
            proxy_pass=proxy_pass,
            enable_proxy=self.widget_proxy.isEnabled(),
            proxy_addr=f'{self.lineEdit_proxy_addr.text()}:{self.lineEdit_proxy_port.text()}',
        )

    def _test(self):
        data = self.data
        url = parse.urljoin(data['proxy_pass'], '/v1/chat/completions')
        body = json.dumps({
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "只回复我两个字'你好'"}],
            "stream": False,
            "temperature": 0,
        }).encode()
        if data['enable_proxy']:
            opener = request.build_opener(request.ProxyHandler({'http': f"http://{data['proxy_addr']}"}))
        else:
            opener = request.build_opener()
        opener.addheaders.append(('Authorization', data['apikey']))
        try:
            resp = opener.open(url, data=body, timeout=3.0)
            if resp.getcode() == 200:
                QMessageBox.information(self, '测试连接', '连接成功')
                return
        except error.URLError:
            pass
        QMessageBox.critical(self, '测试连接', '连接失败')

    def _next(self):
        next_window = Form2()
        next_window.show()
        self.close()
