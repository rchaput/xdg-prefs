"""
This module defines functions and class to handle the Application Database
(i.e. the list of Desktop Entries that represent applications).
"""


import os
import logging

from xdgprefs.core.os_env import xdg_data_dirs
from xdgprefs.core import desktop_entry_parser as parser


def app_dirs(only_existing=True):
    """
    List all the application directories.

    Application directories are the `application` subdirectory in each
    of the XDG_DATA_DIRS directories.

    :param only_existing: If set to `True`, only the existing directories
        will be returned. Otherwise, all possible locations are listed.

    :return: A list of paths.
    """
    dirs = xdg_data_dirs()
    dirs = [os.path.join(d, 'applications/') for d in dirs]
    if only_existing:
        dirs = [d for d in dirs if os.path.exists(d)]
    return dirs


class AppDatabase(object):

    def __init__(self):
        self.logger = logging.getLogger('AppDatabase')
        self.apps = {}

        self._build_db()

    def _build_db(self):
        self.logger.debug('Building the App Database...')
        # First, loop on all applications directories
        for app_dir in app_dirs():
            self.logger.debug(f'Looking in {app_dir}...')
            # Next, loop on each file (recursively)
            for (dirpath, _, filenames) in os.walk(app_dir):
                for filename in filenames:
                    if filename.endswith('.desktop'):
                        filepath = os.path.join(dirpath, filename)
                        _id = os.path.relpath(filepath, app_dir)
                        app = parser.parse(filepath, _id)
                        self._add_app(app)

    def _add_app(self, app):
        if app is not None:
            self.apps[app.appid] = app

    def get_app(self, appid):
        if appid in self.apps:
            return self.apps[appid]
        else:
            return None

    @property
    def size(self):
        return len(self.apps)

    def __str__(self):
        return f'<AppDatabase size={self.size}>'
