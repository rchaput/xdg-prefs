# -*- coding: future_fstrings -*-
"""
This module defines Qt Widgets that allow to view the list of applications
as a Qt List (using a custom widget for the layout).
"""


from PySide2.QtWidgets import QListWidget, QWidget, \
    QLabel, QGridLayout, QLineEdit, QCheckBox

from xdgprefs.core import DesktopEntry
from xdgprefs.gui.app_item import AppItem


class AppsPanel(QWidget):
    """
    This class defines the Qt List that will show all applications.
    """

    def __init__(self, appdb):
        QWidget.__init__(self)

        self.appdb = appdb
        self.app_map = {}

        self.setup_ui()

        for app in self.appdb.apps.values():
            item = AppItem(app, self.list_widget)
            self.app_map[app] = item
            self.list_widget.addItem(item)

        self.setLayout(self.grid)

        self.on_filter_update()

    # noinspection PyAttributeOutsideInit
    def setup_ui(self):
        self.grid = QGridLayout()

        self.edit_search = QLineEdit(self)
        self.edit_search.setPlaceholderText("Type to filter")
        self.edit_search.textChanged.connect(self.on_filter_update)

        self.checkbox_mimetype = QCheckBox(self)
        self.checkbox_mimetype.setText("Include apps without Mime types")
        self.checkbox_mimetype.setChecked(False)
        self.checkbox_mimetype.stateChanged.connect(self.on_filter_update)

        self.checkbox_vendor = QCheckBox(self)
        self.checkbox_vendor.setText("Include vendor apps (vnd-*)")
        self.checkbox_vendor.setChecked(True)
        self.checkbox_vendor.stateChanged.connect(self.on_filter_update)

        self.checkbox_ext = QCheckBox(self)
        self.checkbox_ext.setText("Include extensions apps (x-*)")
        self.checkbox_ext.setChecked(True)
        self.checkbox_ext.stateChanged.connect(self.on_filter_update)

        self.text_status = QLabel(self)

        self.list_widget = QListWidget(self)
        self.list_widget.setSelectionMode(QListWidget.NoSelection)
        self.list_widget.setAlternatingRowColors(True)
        self.list_widget.setStyleSheet('''
                    QListView::item {
                        border: 1px solid #e0e0eb;
                    }
                ''')

        self.grid.addWidget(self.edit_search, 0, 1, 1, 3)
        self.grid.addWidget(self.checkbox_mimetype, 1, 1, 1, 1)
        self.grid.addWidget(self.checkbox_vendor, 1, 2, 1, 1)
        self.grid.addWidget(self.checkbox_ext, 1, 3, 1, 1)
        self.grid.addWidget(self.text_status, 2, 1, 1, 3)
        self.grid.addWidget(self.list_widget, 3, 1, 1, 3)

    def on_filter_update(self):
        filter_text = self.edit_search.text()
        mimetype = self.checkbox_mimetype.isChecked()
        vendor = self.checkbox_vendor.isChecked()
        ext = self.checkbox_ext.isChecked()

        nb_shown = 0
        nb_total = 0
        for app in self.app_map:
            matches = self.matches(app, filter_text, mimetype, vendor, ext)
            # If it matches, show it
            self.app_map[app].setHidden(not matches)
            # Count the number of shown apps
            nb_shown += int(matches)
            nb_total += 1
        self.update_text(nb_shown, nb_total)

    def matches(self,
                app: DesktopEntry,
                filter_text: str,
                mimetype_check: bool,
                vendor_check: bool,
                ext_check: bool):
        if not mimetype_check and \
                (app.mime_type is None or len(app.mime_type) == 0):
            return False
        if not vendor_check and app.is_vendor:
            return False
        if not ext_check and app.is_extension:
            return False
        if app.name.find(filter_text) == -1:
            return False
        return True

    def update_text(self, nb_shown, nb_total):
        text = f'Applications shown: {nb_shown} / {nb_total}'
        self.text_status.setText(text)
