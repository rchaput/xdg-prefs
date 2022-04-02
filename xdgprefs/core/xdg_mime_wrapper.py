"""
This module defines wrapper functions for the `xdg-mime` software.

These functions can be used to query the user preferences (i.e. which desktop
application should be used to open a given media type) and to update them.
"""
import shutil
import subprocess
import logging


logger = logging.getLogger('XdgMimeWrapper')


def _find_xdg_mime():
    """Find the path to the `xdg-mime` executable."""
    # Try to find the `xdg-mime` executable using `which`.
    path = _try_which()
    if path is not None:
        logger.info(f'xdg-mime found at {path}')
        # Check if the executable works.
        ret = _try_path(path)
        if not ret:
            logger.warning(f'which found xdg-mime at {path} but the'
                           f'executable seems not to be working!')
        return path

    # Nothing was found!
    logger.error('xdg-mime was not found on this computer! Impossible to get'
                 'or set the media type associations.')
    return None


def _try_which():
    """Try to find `xdg-mime` using the `which` function (in `shutil`)."""
    return shutil.which('xdg-mime')


def _try_path(path):
    """Try an absolute or relative path for the `xdg-mime` executable."""
    try:
        res = subprocess.run([path, '--version'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             universal_newlines=True)
        if res.returncode is not 0:
            logger.warning(f'Unknown error for path {path} ({res.returncode}):'
                           f' {res.stderr}')
            return False
    except FileNotFoundError:
        logger.warning(f'File not found: {path}')
        return False
    except PermissionError:
        logger.warning(f'File is not executable: {path}')
        return False
    return True


bin_path = _find_xdg_mime()
logger.debug(f'Found xdg-mime: {bin_path}')


def get_default_app(mime_type):
    """
    Get the application that is registered as 'default' to open the
    specified MIME Type.

    :param mime_type: The identifier of the MIME Type, e.g. 'image/jpeg'.
    :type mime_type: str

    :return: The identifier of the desktop application, e.g. 'gimp.desktop'.
    :rtype: str
    """
    if bin_path is None:
        logger.error('Can\'t get the default app if xdg-mime was not found!')
        return None
    res = subprocess.run([bin_path, 'query', 'default', mime_type],
                         capture_output=True,
                         text=True)
    if res.returncode is not 0:
        logger.warning(f'Unknown error while querying default application'
                       f' ({res.returncode}): {res.stderr}')
        return None
    return res.stdout.replace('\n', '')


def set_default_app(mime_type, app):
    """
    Set the default application to open the specified MIME Type.

    :param mime_type: The identifier of the MIME Type, e.g. 'image/jpeg'.
    :type mime_type: str

    :param app: The identifier of the desktop application, e.g. 'gimp.desktop'.
    :type: str

    :return: True if the application was correctly registered as the
    default one (according to the xdg-mime backend, i.e. if the return code
    was 0), False otherwise.
    """
    if bin_path is None:
        logger.critical('Can\t set the default app if xdg-mime was not found!')
        return False
    res = subprocess.run([bin_path, 'default', app, mime_type],
                         capture_output=True,
                         text=True)
    if res.returncode is not 0:
        logger.error(f'Unknown error while setting default application'
                     f' ({res.returncode}): {res.stderr}')
    return res.returncode is 0
