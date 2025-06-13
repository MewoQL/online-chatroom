import sys
from PyQt6.QtWidgets import QApplication
from log import log

if __name__ == '__main__':
    app = QApplication(sys.argv)
    l = log()
    l.show()
    sys.exit(app.exec())

