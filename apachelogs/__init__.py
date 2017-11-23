"""
Parse Apache access logs

Visit <https://github.com/jwodder/apachelogs> for more information.
"""

__version__      = '0.1.0.dev1'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'apachelogs@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/apachelogs'

from .errors import Error, InvalidEntryError, InvalidFormatError
from .format import COMMON, COMMON_VHOST, COMBINED, REFERER, AGENT
from .parser import LogEntry, LogFormat
from .util   import parse_apache_timestamp

__all__ = [
    'AGENT',
    'COMBINED',
    'COMMON',
    'COMMON_VHOST',
    'Error',
    'InvalidEntryError',
    'InvalidFormatError',
    'LogEntry',
    'LogFormat',
    'REFERER',
    'parse_apache_timestamp',
]
