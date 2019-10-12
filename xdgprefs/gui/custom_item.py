"""
This module defines a custom QListWidgetItem that uses the following layout:
- icon on the left
- first line of text, bold
- second line of text
- third line of thext, italic
This QListWidgetItem is used to show both MimeTypes and App.
"""


from PySide2.QtWidgets import QListWidgetItem, QWidget, \
    QVBoxLayout, QHBoxLayout, QLabel
from PySide2.QtGui import QPixmap
from PySide2.QtCore import QSize


class CustomItem(QListWidgetItem):
    """
    This class defines a single item of the list.
    """

    icon_size = QSize(64, 64)

    def __init__(self, listview, first, second, third, icon):
        """
        :param listview: The parent ListView.
        :param first: The first line of text.
        :param second: The second line of text.
        :param third: The third line of text.
        :param icon: The full path to the icon.
        """
        QListWidgetItem.__init__(self, listview, type=QListWidgetItem.UserType)

        self.widget = QWidget()

        # Vertical box (texts)
        self.vbox = QVBoxLayout()

        self.first_line = QLabel(first)
        self.first_line.setWordWrap(True)

        self.second_line = QLabel(second)
        self.second_line.setWordWrap(True)

        self.third_line = QLabel(third)
        self.third_line.setWordWrap(True)

        for widget in [self.first_line, self.second_line, self.third_line]:
            self.vbox.addWidget(widget)

        # Horizontal box (icon + vertical box)
        self.hbox = QHBoxLayout()

        self.icon = QLabel()
        pixmap = QPixmap(icon)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(CustomItem.icon_size)
        self.icon.setPixmap(pixmap)

        self.hbox.addWidget(self.icon, 0)
        self.hbox.addLayout(self.vbox, 1)

        self.widget.setLayout(self.hbox)

        # Set the widget as the content of the list item
        self.setSizeHint(self.widget.sizeHint())
        listview.setItemWidget(self, self.widget)

        self.first_line.setStyleSheet('''font-weight: bold;''')
        # self.comment.setStyleSheet('''''')
        self.third_line.setStyleSheet('''font-style: italic;''')
