import sys

from PyQt6.QtWidgets import QApplication

from ui.Form1 import Form1


def main():
    app = QApplication(sys.argv)
    form = Form1()
    form.show()
    try:
        sys.exit(app.exec())
    except KeyboardInterrupt:
        sys.exit(-1)
