"""
This module defines the MimeType class as well as a MimeTypeParser (used
to parse media types from their XML files).
"""


import logging
from typing import List
from xml.etree import ElementTree

from xdgprefs import os_env


class MimeType(object):
    """
    Defines a MIME Type (or Media Type).

    Media Types are defined in the following RFC:

    - https://tools.ietf.org/html/rfc2045
    - https://tools.ietf.org/html/rfc6838
    """

    def __init__(self,
                 _type: str,
                 subtype: str,
                 comment: str,
                 extensions: List[str]):
        # Data
        self.type = _type
        self.subtype = subtype
        self.comment = comment
        self.extensions = extensions

        # Computed data
        self.identifier = '{}/{}'.format(self.type, self.subtype)

    @property
    def is_extension(self):
        return self.subtype.startswith('x-') \
               or self.subtype.startswith('x.')

    @property
    def is_vendor(self):
        return self.subtype.startswith('vnd-') \
               or self.subtype.startswith('vnd.')

    @property
    def is_personal(self):
        return self.subtype.startswith('prs-') \
               or self.subtype.startswith('prs.')

    def __repr__(self):
        return self.identifier

    def __str__(self):
        return '{}/{} ({})'.format(self.type, self.subtype, self.comment)


class MimeTypeParser:

    logger = logging.getLogger('MimeTypeParser')
    xmlns = '{http://www.freedesktop.org/standards/shared-mime-info}'

    @classmethod
    def parse(cls, filepath):
        tree = ElementTree.parse(filepath)
        # The root element represents a Mime Type
        root = tree.getroot()
        if not cls._check_tag(filepath, root):
            return None
        if not cls._check_attrib(filepath, root):
            return None
        _type, subtype = cls._get_type_subtype(root)
        comment = cls._get_comment(root)
        extensions = cls._get_extensions(root)
        return MimeType(_type, subtype, comment, extensions)

    @classmethod
    def _check_tag(cls, filepath, root):
        correct = f'{cls.xmlns}mime-type'
        if root.tag != correct:
            cls.logger.warning(f'The root element of {filepath} is '
                               f'{root.tag}, should be {correct}! Ignoring '
                               f'this file.')
            return False
        return True

    @classmethod
    def _check_attrib(cls, filepath, root):
        if 'type' not in root.attrib:
            cls.logger.warning(f'The root element of {filepath} does not '
                               f'have a type attribute! Ignoring this file.')
            return False
        return True

    @classmethod
    def _get_type_subtype(cls, root):
        identifier = root.attrib['type']
        _type, subtype = identifier.split('/')
        return _type, subtype

    @classmethod
    def _get_comment(cls, root):
        comments = root.findall(f'{cls.xmlns}comment')
        os_lang = os_env.get_language()
        # TODO: pick the comment matching the OS lang instead of the default
        for comment in comments:
            comment_lang = comment.attrib['lang'] \
                if 'lang' in comment.attrib else ''
            if comment_lang == '':
                return comment.text
        return ''

    @classmethod
    def _get_extensions(cls, root):
        extensions = []
        for glob in root.findall(f'{cls.xmlns}glob'):
            if 'pattern' in glob.attrib:
                extensions.append(glob.attrib['pattern'])
        return extensions
