"""
This module defines a single Application Item in the AppsPanel.
"""


from xdgprefs.gui.custom_item import CustomItem


def _get_icon(icon_name):
    """Return the path to an icon."""
    theme = 'Adwaita'
    size = '256x256'
    path = f'/usr/share/icons/{theme}/{size}/mimetypes/{icon_name}.png'
    return path


def _get_types(type_list):
    if type_list is None:
        return ''
    else:
        return ', '.join(type_list)


class AppItem(CustomItem):

    def __init__(self, app, listview):
        CustomItem.__init__(self, listview,
                            app.name,
                            app.comment,
                            _get_types(app.mime_type),
                            _get_icon(app.icon))
        self.app = app
