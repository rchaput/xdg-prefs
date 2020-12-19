# -*- coding: future_fstrings -*-
"""
This module defines the database that lists associations between
MIME Types and Applications (represented by Desktop Entries).

This database can be used to view and to change such associations
(e.g. the default application used to open a given MIME Type).

https://specifications.freedesktop.org/mime-apps-spec/latest/index.html
"""


import configparser
import logging
import os
from collections import defaultdict

from xdgprefs.core import os_env


ADDED = 'Added Applications'
REMOVED = 'Removed Applications'
DEFAULT = 'Default Applications'
CACHE = 'MIME Cache'


class Associations(object):

    def __init__(self):
        self.added = []
        self.removed = []
        self.default = []

    def extend_added(self, apps):
        for app in apps:
            if app not in self.added and app not in self.removed:
                self.added.append(app)

    def extend_removed(self, apps):
        for app in apps:
            if app not in self.removed:
                self.removed.append(app)

    def extend_default(self, apps):
        for app in apps:
            if app not in self.default:
                self.default.append(app)


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
    for _dir in dirs:
        for prefix in prefixes:
            file = os.path.join(_dir, prefix + 'mimeinfo.cache')
            files.append(file)

    if only_existing:
        files = [f for f in files if os.path.exists(f)]

    return files


class ArrayInterpolation(configparser.Interpolation):

    def before_read(self, parser, section, option, value):
        values = value.split(';')
        # if the line is 'd1;d2;', the last element is empty, let's remove it
        if values[-1].strip() == '':
            values.pop(-1)
        return values

    def before_write(self, parser, section, option, value):
        return ';'.join(value) + ';'


def parse_mimeapps(file_path):
    config = configparser.ConfigParser(delimiters='=',
                                       interpolation=ArrayInterpolation(),
                                       strict=False)
    try:
        config.read(file_path)
        for section in [ADDED, REMOVED, DEFAULT]:
            if section not in config.sections():
                config[section] = {}
        return config
    except configparser.Error as e:
        print(e)
        return None


class AssociationsDatabase(object):

    def __init__(self):
        self.logger = logging.getLogger('AssociationsDatabase')
        self.associations = defaultdict(Associations)
        self.config_path = os.path.join(os_env.xdg_config_home(),
                                        'mimeapps.list')
        self.config = parse_mimeapps(self.config_path)

        self._build_db()

    def _build_db(self):
        files = mimeapps_files(True)
        for file in files:
            self._parse_mimeapps_file(file)
        files = cache_files(True)
        for file in files:
            self._parse_cache_file(file)

    def _parse_mimeapps_file(self, path):
        config = parse_mimeapps(path)
        if config is None:
            self.logger.warning(f'Badly formatted file: {path}')
            return
        section = config[ADDED]
        for mimetype, apps in section.items():
            self.associations[mimetype].extend_added(apps)
        section = config[REMOVED]
        for mimetype, apps in section.items():
            self.associations[mimetype].extend_removed(apps)
        section = config[DEFAULT]
        for mimetype, apps in section.items():
            self.associations[mimetype].extend_default(apps)

    def _parse_cache_file(self, path):
        config = parse_mimeapps(path)
        if config is None:
            self.logger.warning(f'Badly formatted file: {path}')
            return
        for mimetype, apps in config[CACHE].items():
            assoc = self.associations[mimetype]
            assoc.extend_default(apps)

    def get_apps_for_mimetype(self, mimetype):
        if mimetype in self.associations:
            assoc = self.associations[mimetype]
            return assoc.default
        return []

    def set_app_for_mimetype(self, mimetype, app):
        section = self.config[DEFAULT]
        apps = section.get(mimetype, fallback=[])
        if app in apps:
            apps.remove(app)
        apps.insert(0, app)
        return self.save_config()

    def save_config(self):
        try:
            with open(self.config_path, 'w') as f:
                self.config.write(f, space_around_delimiters=False)
            return True
        except:
            return False

    @property
    def size(self):
        return len(self.associations)
