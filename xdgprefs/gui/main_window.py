"""
This module defines the main window, allowing the user to effectively
use the application.
"""


from PySide6.QtWidgets import QMainWindow, QTabWidget

from xdgprefs.gui import MimeTypePanel, AppsPanel, AssociationsPanel
from xdgprefs.core import MimeDatabase, AppDatabase, AssociationsDatabase


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('xdg-prefs')

        # Back-end data
        self.mimedb = MimeDatabase()
        self.appdb = AppDatabase()
        self.assocdb = AssociationsDatabase()

        # Set size
        self.resize(400, 600)

        # Menu
        self.menu = self.menuBar()
        # self.help_menu = self.menu.addMenu('Help')

        # Status
        self.status = self.statusBar()
        self.status.showMessage('No log')

        # Central widget
        self.central = QTabWidget(self)
        # First tab
        self.page1 = AssociationsPanel(self)
        self.central.addTab(self.page1, 'Associations')
        # Second tab
        self.page2 = MimeTypePanel(self.mimedb)
        self.central.addTab(self.page2, 'List MIME Types')
        # Third tab
        self.page3 = AppsPanel(self.appdb)
        self.central.addTab(self.page3, 'List Applications')

        self.setCentralWidget(self.central)

        self.show()
