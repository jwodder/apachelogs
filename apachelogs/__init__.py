"""
Parse Apache access logs

Visit <https://github.com/jwodder/apachelogs> for more information.
"""

__version__      = '0.1.0.dev1'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'apachelogs@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/apachelogs'

from .errors import Error, InvalidDirectiveError, InvalidEntryError, \
                    UnknownDirectiveError
from .parser import LogEntry, LogParser
from .util   import parse_apache_timestamp

__all__ = [
    'AGENT',
    'COMBINED',
    'COMMON',
    'COMMON_VHOST',
    'Error',
    'InvalidDirectiveError',
    'InvalidEntryError',
    'LogEntry',
    'LogParser',
    'REFERER',
    'UnknownDirectiveError',
    'parse',
    'parse_apache_timestamp',
    'parse_lines',
]

### cf. the log definitions shipped with Apache under Ubuntu (Debian?), which
### use %O instead of %b

#: Common log format (CLF)
COMMON = "%h %l %u %t \"%r\" %>s %b"

#: Common log format with virtual host prepended
COMMON_VHOST = "%v %h %l %u %t \"%r\" %>s %b"

#: NCSA extended/combined log format
COMBINED = "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\""

def parse(format, entry, encoding='iso-8859-1', errors=None):
    """
    A convenience function for parsing a single logfile entry without having
    to directly create a `LogParser` object.

    ``encoding`` and ``errors`` have the same meaning as for `LogParser`.
    """
    return LogParser(format, encoding=encoding, errors=errors).parse(entry)

def parse_lines(format, entries, encoding='iso-8859-1', errors=None,
                ignore_invalid=False):
    """
    A convenience function for parsing an iterable of logfile entries without
    having to directly create a `LogParser` object.

    ``encoding`` and ``errors`` have the same meaning as for `LogParser`.
    ``ignore_invalid`` has the same meaning as for `LogParser.parse_lines()`.
    """
    return LogParser(format, encoding=encoding, errors=errors)\
        .parse_lines(entries, ignore_invalid)
