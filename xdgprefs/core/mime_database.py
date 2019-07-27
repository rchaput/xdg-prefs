"""
This module provides functions and classes used to handle the Mime Database
(i.e. the set of known MIME Types, with associated meta information).

https://www.linuxtopia.org/online_books/linux_desktop_guides/gnome_2.14_admin_guide/mimetypes-database.html
"""


import os
import logging
from typing import Dict

from xdgprefs.core.os_env import xdg_data_dirs, xdg_data_home
from xdgprefs.core.mime_type import MimeType, MimeTypeParser


def mime_dirs(only_existing=True):
    """
    List all the MIME directories.

    MIME directories are the `mime` subdirectory in each of the
    XDG_DATA_HOME:XDG_DATA_DIRS directories, noted <MIME> in the
    specifications.

    :arg only_existing: If set to `True`, only the existing directories will
        be returned. Otherwise, all possible locations are listed.

    :return: A list of paths.
    """
    home = xdg_data_home()
    dirs = [home] + xdg_data_dirs()
    dirs = [os.path.join(d, 'mime') for d in dirs]
    if only_existing:
        dirs = [d for d in dirs if os.path.exists(d)]
    return dirs


class MimeDatabase(object):
    """
    This class finds and holds all Media Types registered on the computer.

    It is used to build the database in a first step, and then query it.
    """

    logger: logging.Logger
    types: Dict[str, MimeType]

    def __init__(self):
        self.logger = logging.getLogger('MimeDatabase')
        self.types = {}

        self._build_db()

    def _build_db(self):
        """Build the database, searching in the <MIME> directories."""
        self.logger.debug('Building the Mime Database...')
        # First, loop on all <MIME> directories.
        for mime_dir in mime_dirs():
            self.logger.debug(f'Looking in {mime_dir}...')
            # Next, loop on the <MEDIA> subdirectories.
            # Ignore the `packages` subdirectory (not a MEDIA).
            subdirs = [f.path for f in os.scandir(mime_dir) if f.is_dir()
                       and f.name != 'packages']
            for media_dir in subdirs:
                # Loop on each file (describing a Mime Type)
                files = [f.path for f in os.scandir(media_dir) if f.is_file()]
                for filepath in files:
                    mimetype = MimeTypeParser.parse(filepath)
                    self._add_type(mimetype)

    def _add_type(self, mimetype):
        """Adds a MimeType to the database."""
        if mimetype is None:
            return
        if mimetype.identifier in self.types:
            self.logger.warning(f'MimeType {mimetype.identifier} already '
                                f'in the database, overwriting!')
        self.types[mimetype.identifier] = mimetype

    def get_type(self, identifier):
        """Return the MimeType associated to an identifier."""
        if identifier in self.types:
            return self.types[identifier]
        else:
            return None

    @property
    def size(self):
        return len(self.types)

    def __str__(self):
        return f'<MimeDatabase size={self.size}>'
