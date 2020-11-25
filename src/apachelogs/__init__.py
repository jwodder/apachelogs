r"""
Parse Apache access logs

``apachelogs`` parses Apache access log files.  Pass it a `log format string
<http://httpd.apache.org/docs/current/mod/mod_log_config.html>`_ and get back a
parser for logfile entries in that format.  ``apachelogs`` even takes care of
decoding escape sequences and converting things like timestamps, integers, and
bare hyphens to ``datetime`` values, ``int``\s, and ``None``\s.

Visit <https://github.com/jwodder/apachelogs> or <https://apachelogs.rtfd.io>
for more information.
"""

__version__      = '0.7.0.dev1'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'apachelogs@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/apachelogs'

from .errors   import Error, InvalidDirectiveError, InvalidEntryError, \
                      UnknownDirectiveError
from .parser   import LogEntry, LogParser
from .timeutil import parse_apache_timestamp

__all__ = [
    'COMBINED',
    'COMBINED_DEBIAN',
    'COMMON',
    'COMMON_DEBIAN',
    'Error',
    'InvalidDirectiveError',
    'InvalidEntryError',
    'LogEntry',
    'LogParser',
    'UnknownDirectiveError',
    'VHOST_COMBINED',
    'VHOST_COMMON',
    'parse',
    'parse_apache_timestamp',
    'parse_lines',
]

#: Common log format (CLF)
COMMON = "%h %l %u %t \"%r\" %>s %b"

#: `COMMON` with virtual host prepended
VHOST_COMMON = "%v %h %l %u %t \"%r\" %>s %b"

#: NCSA extended/combined log format
COMBINED = "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\""

#: Like `COMMON`, but with ``%O`` (total bytes sent including headers) in place
#: of ``%b`` (size of response excluding headers)
COMMON_DEBIAN = "%h %l %u %t \"%r\" %>s %O"

#: Like `COMBINED`, but with ``%O`` (total bytes sent including headers) in
#: place of ``%b`` (size of response excluding headers)
COMBINED_DEBIAN = "%h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\""

#: `COMBINED_DEBIAN` with virtual host & port prepended
VHOST_COMBINED = "%v:%p %h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\""

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
