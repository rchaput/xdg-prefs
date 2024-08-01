"""
This module defines a single MimeTypeItem in the MimeTypePanel.
"""


from xdgprefs.gui.custom_item import CustomItem


def _get_icon(icon_name):
    """Return the path to an icon."""
    theme = 'Adwaita'
    size = '256x256'
    path = f'/usr/share/icons/{theme}/{size}/mimetypes/{icon_name}.png'
    return path


def _get_extensions(ext_list):
    if ext_list is None:
        return ''
    else:
        return ', '.join(ext_list)


class MimeTypeItem(CustomItem):

    def __init__(self, mime_type, listview):
        CustomItem.__init__(self, listview,
                            mime_type.identifier,
                            mime_type.comment,
                            _get_extensions(mime_type.extensions),
                            _get_icon(mime_type.icon))
        self.mime_type = mime_type
