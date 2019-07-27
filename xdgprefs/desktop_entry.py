"""
This module defines code relative to Desktop Entries, i.e. applications
which are compliant with the XDG specifications.

https://specifications.freedesktop.org/desktop-entry-spec/latest/
"""

import logging
from collections import defaultdict
from typing import Optional


class Entry(object):
    """
    An Entry, i.e. a single line of a Desktop Entry file.

    Such entries have a key, a value, and an optional locale:
    Key[Locale]=Value
    """

    def __init__(self, key: str,
                 value: str,
                 locale: Optional[str]):
        self.key = key
        self.value = value
        self.locale = locale


class EntryGroup(object):
    """
    An Entry Group, i.e. a set of unique entries identified by (key,locale).
    """

    def __init__(self, name: str):
        self.name = name
        self.entries = defaultdict(lambda: defaultdict(lambda: None))

    def add_entry(self, entry: Entry):
        """Add an entry to the group."""
        self.entries[entry.key][entry.locale] = entry

    def get_entry(self, entry_key, entry_locale=None) -> Optional[Entry]:
        """Return an entry identified by its key and locale, or None."""
        entries = self.entries[entry_key]
        # TODO: search the best matching locale.
        if entry_locale is not None and entry_locale not in entries:
            # The specified locale is not found, so we use the default one.
            return entries[None]
        else:
            return entries[entry_locale]

    def get_entry_value(self, entry_key, entry_locale=None):
        """Return the value of an entry, or None."""
        entry = self.get_entry(entry_key, entry_locale)
        return entry.value if entry is not None else None


class DesktopEntry(object):
    """
    A Desktop Entry file defines an application, and is composed of multiple
    Entry Groups. The default one is named 'Desktop Entry'.
    """

    def __init__(self, groups, appid):
        self.groups = groups
        self.appid = appid
        self.logger = logging.getLogger('DesktopEntry-' + appid)

    def get_entry(self, entry_key, groupname='Desktop Entry'):
        if groupname not in self.groups:
            self.logger.warning(f'Group name {groupname} not found!')
            return None
        group = self.groups[groupname]
        return group.get_entry(entry_key)

    def get_entry_value(self, entry_key, groupname='Desktop Entry'):
        entry = self.get_entry(entry_key, groupname)
        return entry.value if entry is not None else None

    @property
    def name(self):
        return self.get_entry_value('Name')

    @property
    def generic_name(self):
        return self.get_entry_value('GenericName')

    @property
    def icon(self):
        return self.get_entry_value('Icon')

    @property
    def hidden(self):
        return self.get_entry_value('Hidden')

    @property
    def only_show_in(self):
        return self.get_entry_value('OnlyShowIn')

    @property
    def not_show_in(self):
        return self.get_entry_value('NotShowIn')

    @property
    def mime_type(self):
        return self.get_entry_value('MimeType')
