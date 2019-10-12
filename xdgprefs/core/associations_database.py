"""
This module defines the database that lists associations between
MIME Types and Applications (represented by Desktop Entries).

This database can be used to view and to change such associations
(e.g. the default application used to open a given MIME Type).

https://specifications.freedesktop.org/mime-apps-spec/latest/index.html
"""


import logging
import os
from collections import defaultdict
from enum import Enum, auto

from xdgprefs.core import os_env


class Associations(object):

    def __init__(self):
        self.added = []
        self.removed = []
        self.default = []


class Section(Enum):
    ADDED = auto()
    REMOVED = auto()
    DEFAULT = auto()


def mimeapps_files(only_existing=True):
    desktop = os_env.get_current_desktop_environment()
    prefixes = [''] + [name + '-' for name in desktop]
    config_home = os_env.xdg_config_home()
    config_dirs = os_env.xdg_config_dirs()
    data_home = os_env.xdg_data_home()
    data_dirs = os_env.xdg_data_dirs()

    files = []

    # CONFIG_HOME
    for prefix in prefixes:
        path = os.path.join(config_home, prefix + 'mimeapps.list')
        files.append(path)

    # CONFIG_DIRS
    for directory in config_dirs:
        for prefix in prefixes:
            path = os.path.join(directory, prefix + 'mimeapps.list')
            files.append(path)

    # DATA_HOME
    for prefix in prefixes:
        path = os.path.join(data_home, 'applications', prefix + 'mimeapps.list')
        files.append(path)

    # DATA_DIRS
    for directory in data_dirs:
        for prefix in prefixes:
            path = os.path.join(directory, 'applications',
                                prefix + 'mimeapps.list')
            files.append(path)

    if only_existing:
        files = [f for f in files if os.path.exists(f)]
    return files


def cache_files(only_existing=True):
    desktop = os_env.get_current_desktop_environment()
    prefixes = [''] + [name + '-' for name in desktop]

    dirs = [os_env.xdg_data_home()] + os_env.xdg_data_dirs()
    dirs = [os.path.join(d, 'applications') for d in dirs]

    files = []
    for dir in dirs:
        for prefix in prefixes:
            file = os.path.join(dir, prefix + 'mimeinfo.cache')
            files.append(file)

    if only_existing:
        files = [f for f in files if os.path.exists(f)]

    return files


def extend_blacklist(list1, list2, blacklist):
    """
    Extend a list with the contents of another list, except for those
    in the blacklist.
    """
    for elt in list2:
        if elt not in blacklist:
            list1.append(elt)


def extend_unique(list1, list2):
    """
    Extend a list with the elements of another list which are not
    already in the first list.
    """
    extend_blacklist(list1, list2, list1)


class AssociationsDatabase(object):

    def __init__(self):
        self.logger = logging.getLogger('AssociationsDatabase')
        self.associations = defaultdict(Associations)

        self._build_db()

    def _build_db(self):
        files = mimeapps_files(True)
        for file in files:
            self._parse_mimeapps_file(file)
        files = cache_files(True)
        for file in files:
            self._parse_cache_file(file)

    def _parse_mimeapps_file(self, path):
        with open(path, 'r') as f:
            section = None
            for line in f.readlines():
                line = line.strip()
                if line == '':
                    continue
                if line == '[Added Associations]':
                    section = Section.ADDED
                elif line == '[Removed Associations]':
                    section = Section.REMOVED
                elif line == '[Default Applications]':
                    section = Section.DEFAULT
                else:
                    mimetype, apps = self._parse_line(line)
                    assoc = self.associations[mimetype]
                    if section is Section.ADDED:
                        extend_blacklist(assoc.added, apps, assoc.removed)
                        # for app in apps:
                        #     if app not in assoc.removed:
                        #         assoc.added.append(app)
                    elif section is Section.REMOVED:
                        extend_unique(assoc.removed, apps)
                    elif section is Section.DEFAULT:
                        extend_unique(assoc.default, apps)
                    else:
                        self.logger.warning(f'Badly formatted file: {path}')

    def _parse_cache_file(self, path):
        with open(path, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if '=' in line:
                    mimetype, apps = self._parse_line(line)
                    assoc = self.associations[mimetype]
                    assoc.default.extend(apps)

    def _parse_line(self, line):
        mimetype, apps = line.split('=')
        apps = apps.split(';')
        if apps[-1] == '':
            apps.remove('')
        return mimetype, apps

    def get_apps_for_mimetype(self, mimetype):
        if mimetype in self.associations:
            assoc = self.associations[mimetype]
            return assoc.default
        return []

    def get_mimetypes_for_app(self, app):
        return []

    @property
    def size(self):
        return len(self.associations)
