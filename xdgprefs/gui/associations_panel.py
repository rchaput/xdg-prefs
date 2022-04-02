"""
This modules defines widgets that allow to view the associations between
MIME Types and Applications as a Qt List, and to modify the associated
application for each MIME Type.
"""


from PySide2.QtWidgets import QListWidget, QWidget, \
    QLabel, QCheckBox, QLineEdit, QGridLayout

from xdgprefs.core import MimeType
from xdgprefs.gui.association_item import AssociationItem


class AssociationsPanel(QWidget):
    """
    This class defines the Qt List that will show all Mime Types.
    """

    def __init__(self, main_window):
        QWidget.__init__(self)

        self.assocdb = main_window.assocdb
        self.mimedb = main_window.mimedb
        self.appdb = main_window.appdb

        self.item_map = {}

        self.setup_ui()

        for mime_id in self.assocdb.associations.keys():
            mime = self.mimedb.get_type(mime_id)
            if mime is not None:
                apps = self.assocdb.get_apps_for_mimetype(mime_id)
                item = AssociationItem(mime, apps, main_window,
                                       self.list_widget)
                self.item_map[mime] = item
                self.list_widget.addItem(item)

        self.setLayout(self.grid)

        self.on_filter_update()

    # noinspection PyAttributeOutsideInit
    def setup_ui(self):
        self.grid = QGridLayout()

        self.edit_search = QLineEdit(self)
        self.edit_search.setPlaceholderText("Type to filter")
        self.edit_search.textChanged.connect(self.on_filter_update)

        self.checkbox_personal = QCheckBox(self)
        self.checkbox_personal.setText("Include personal Mime types (prs-*)")
        self.checkbox_personal.setChecked(True)
        self.checkbox_personal.stateChanged.connect(self.on_filter_update)

        self.checkbox_vendor = QCheckBox(self)
        self.checkbox_vendor.setText("Include vendor Mime types (vnd-*)")
        self.checkbox_vendor.setChecked(True)
        self.checkbox_vendor.stateChanged.connect(self.on_filter_update)

        self.checkbox_ext = QCheckBox(self)
        self.checkbox_ext.setText("Include extensions Mime types (x-*)")
        self.checkbox_ext.setChecked(True)
        self.checkbox_ext.stateChanged.connect(self.on_filter_update)

        self.text_status = QLabel(self)

        self.list_widget = QListWidget(self)
        self.list_widget.setSelectionMode(QListWidget.NoSelection)
        self.list_widget.setAlternatingRowColors(True)
        self.list_widget.setStyleSheet('''
                    QListView::item {
                        border: 1px solid #c5c5c5;
                    }
                ''')

        self.grid.addWidget(self.edit_search, 0, 1, 1, 3)
        self.grid.addWidget(self.checkbox_personal, 1, 1, 1, 1)
        self.grid.addWidget(self.checkbox_vendor, 1, 2, 1, 1)
        self.grid.addWidget(self.checkbox_ext, 1, 3, 1, 1)
        self.grid.addWidget(self.text_status, 2, 1, 1, 3)
        self.grid.addWidget(self.list_widget, 3, 1, 1, 3)

    def on_filter_update(self):
        filter_text = self.edit_search.text()
        personal = self.checkbox_personal.isChecked()
        vendor = self.checkbox_vendor.isChecked()
        ext = self.checkbox_ext.isChecked()

        nb_shown = 0
        nb_total = 0
        for mime_type in self.item_map:
            matches = self.matches(mime_type, filter_text, personal, vendor,
                                   ext)
            # If it matches, show it
            self.item_map[mime_type].setHidden(not matches)
            # Count the number of shown apps
            nb_shown += int(matches)
            nb_total += 1
        self.update_text(nb_shown, nb_total)

    def matches(self,
                mime_type: MimeType,
                filter_text: str,
                personal_check: bool,
                vendor_check: bool,
                ext_check: bool):
        if not personal_check and mime_type.is_personal:
            return False
        if not vendor_check and mime_type.is_vendor:
            return False
        if not ext_check and mime_type.is_extension:
            return False
        if mime_type.identifier.find(filter_text) == -1:
            return False
        return True

    def update_text(self, nb_shown, nb_total):
        text = f'Mime types shown: {nb_shown} / {nb_total}'
        self.text_status.setText(text)
