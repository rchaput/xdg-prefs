"""
Desktop file tokenizer and parser.
Source: https://github.com/wor/desktop_file_parser
This work was copied and modified from wor's work (licensed under GPL).
"""

import re
from collections import OrderedDict
import logging

from xdgprefs.desktop_entry import DesktopEntry, EntryGroup, Entry


logger = logging.getLogger('DesktopEntryParser')


def convert_bool(entry: Entry):
    """Try and convert an entry's value to a boolean, or return the value."""
    if entry.value in ['0', 'false']:
        return False
    elif entry.value in ['1', 'true']:
        return True
    else:
        msg = f'Key {entry.key} does not have a boolean value ({entry.value})'
        logger.warning(msg)
        return entry.value


def split(text):
    """Split a text, taking escape characters into account."""
    # See https://stackoverflow.com/a/21882672
    escape = '\\'
    ret = []
    current = []
    itr = iter(text)
    for ch in itr:
        if ch == escape:
            try:
                # skip the next character; it has been escaped!
                current.append(next(itr))
            except StopIteration:
                current.append(escape)
        elif ch == ';' or ch == ',':
            # split! (add current to the list and reset it)
            ret.append(''.join(current))
            current = []
        else:
            current.append(ch)
    if len(current) > 0:
        ret.append(''.join(current))
    return ret


def tok_gen(text):
    """
    Simplified token generator.
    As Desktop files are not really that complex to tokenize, this function
    replaces the tokenizer dependency.

    Parameters:
        text: str. Desktop file as string.
    Returns:
        (str,()).
    """
    reg = r"""(?P<ENTRY>^(.+?)(\[.+?\])?=(.*)$\n?)|"""\
          r"""(?P<COMMENT_LINE>^#(.*)\n)|"""\
          r"""(?P<EMPTY_LINE>^[ \t\r\f\v]*\n)|"""\
          r"""(?P<GROUP_HEADER>^\[(.+?)\]\s*$\n?)"""
    r = re.compile(reg, re.MULTILINE)

    tok_gen.groups = OrderedDict(sorted(r.groupindex.items(),
                                        key=lambda t: t[1]))

    # Make tok_gen.groups contain mapping from regex group name to submatch
    # range. Submatch range start-1 is the whole match.
    last_i = None
    for i in tok_gen.groups.items():
        if last_i is None:
            last_i = i
            continue
        tok_gen.groups[last_i[0]] = (last_i[1], i[1]-1)
        last_i = i
    tok_gen.groups[last_i[0]] = (last_i[1], r.groups)

    pos = 0
    while True:
        m = r.match(text, pos)
        if not m:
            if pos != len(text):
                raise SyntaxError("Tokenization failed!")
            break
        pos = m.end()
        start = tok_gen.groups[m.lastgroup][0]
        end = tok_gen.groups[m.lastgroup][1]
        yield m.lastgroup, m.groups()[start:end]


def parse(filepath, name):
    """
    Parses desktop entry file.

    Args:
        filepath: The complete path to the Desktop Entry file.
        name: The name of the file (e.g. com-mycompany-myapp.desktop)
    Returns:
        DesktopFile. Instance of DesktopFile class which represents the
            parsed desktop file.
    """
    with open(filepath, 'r') as f:
        tokens = tok_gen(f.read())

    # Desktop files entry groups
    entry_groups = {}

    # Refine symbol stream.
    try:
        current_group = None
        for t in tokens:
            tok_name = t[0]
            subvalues = t[1]
            if tok_name == "EMPTY_LINE":
                continue
            elif tok_name == "COMMENT_LINE":
                continue
            elif tok_name == "GROUP_HEADER":
                current_group = subvalues[0]
                entry_groups[current_group] = EntryGroup(current_group)
                continue
            elif tok_name == "ENTRY":
                entry_name = subvalues[0]
                entry_value = subvalues[2]
                entry_locale = subvalues[1].strip("[]") \
                    if subvalues[1] else None
                entry = Entry(entry_name, entry_value, entry_locale)

                # Check boolean entries
                if entry.key in ["NoDisplay", "Hidden", "Terminal",
                                 "StartupNotify", "X-MultipleArgs"]:
                    entry.value = convert_bool(entry)
                # Check multiple string entries (string lists)
                elif entry.key in ["OnlyShowIn", "NotShowIn", "Actions",
                                   "MimeType", "Categories", "Keywords"]:
                    entry.value = split(entry.value)

                entry_groups[current_group].add_entry(entry)
            else:
                msg = f'Token unrecognized while parsing Desktop file: {name}'
                logger.warning(msg)
    except SyntaxError as e:
        msg = f'Syntax error {e} when parsing Desktop file: {name}'
        logger.error(msg)
        return None

    name = name.replace('/', '-')

    df = DesktopEntry(entry_groups, name)
    return df
