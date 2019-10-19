"""
This module defines a single AssociationItem in the AssociationsPanel.
"""


from threading import Thread

from PySide2.QtWidgets import QComboBox

from xdgprefs.gui.mime_item import MimeTypeItem


class AssociationItem(MimeTypeItem):

    def __init__(self, mime_type, apps, main_window, listview):
        MimeTypeItem.__init__(self, mime_type, listview)

        self.apps = apps
        self.main_window = main_window

        self.selector = QComboBox()
        self.selector.addItems(self.apps)
        self.selector.currentTextChanged.connect(self._on_selected)

        self.hbox.addWidget(self.selector, 2)

    def _on_selected(self, text):
        mime = self.mime_type.identifier
        app = self.selector.currentText()
        self.main_window.status.showMessage(f'Setting {mime} to {app}...')
        def run():
            success = self.main_window.assocdb.set_app_for_mimetype(mime, app)
            if success:
                msg = f'{app} was successfully set to open {mime}.'
            else:
                msg = f'Could not set {app} to open {mime}, please check ' \
                      f'the logs!'
            self.main_window.status.showMessage(msg)
        t = Thread(target=run)
        t.start()

    def __hash__(self):
        return hash(self.mime_type)
