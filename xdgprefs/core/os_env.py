"""
This module allows access to various environment variables of the Operating
System, such as XDG configuration values, the current Desktop Environment,
or the language.

XDG values (data directory, configuration directory, ...):
https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
"""


import os


def xdg_data_home():
    """Base directory where user specific data files should be stored."""
    value = os.getenv('XDG_DATA_HOME')
    if value is None or value == '':
        value = '$HOME/.local/share/'
    return os.path.expandvars(value)


def xdg_config_home():
    """Base directory where user specific config files should be stored."""
    value = os.getenv('XDG_CONFIG_HOME')
    if value is None or value == '':
        value = '$HOME/.config/'
    return os.path.expandvars(value)


def xdg_data_dirs():
    """Ordered set of directories for data files."""
    value = os.getenv('XDG_DATA_DIRS')
    if value is None or value == '':
        value = '/usr/local/share/:/usr/share/'
    value = value.split(':')
    return value


def xdg_config_dirs():
    """Ordered set of directories for config files."""
    value = os.getenv('XDG_CONFIG_DIRS')
    if value is None or value == '':
        value = '/etc/xdg/'
    return value.split(':')


def xdg_cache_home():
    """Base directory where user specific cached data should be stored."""
    value = os.getenv('XDG_CACHE_HOME')
    if value is None or value == '':
        value = ''
    return os.path.expandvars(value)


def xdg_runtime_dir():
    """Base directory for runtime files, such as sockets."""
    value = os.getenv('XDG_RUNTIME_DIR')
    return os.path.expandvars(value)


def get_current_desktop_environment():
    """
    Returns an identifier of the current Desktop Environment, such as
    `gnome`, `kde` or `i3`.

    :rtype: str
    """
    return os.getenv('XDG_CURRENT_DESKTOP')


def get_language():
    """
    Returns the BCP47 language from the environment (e.g. `en`).

    https://tools.ietf.org/html/bcp47

    :rtype: str
    """
    lang = os.getenv('LANGUAGE')
    lang = lang.split(':')[1]
    return lang
