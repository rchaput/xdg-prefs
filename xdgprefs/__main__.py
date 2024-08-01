"""
Entry-point of the xdg-prefs software.
"""


import sys
from PySide6.QtWidgets import QApplication

from xdgprefs.gui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
