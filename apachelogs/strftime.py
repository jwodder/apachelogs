# cf. <http://pubs.opengroup.org/onlinepubs/9699919799/functions/strftime.html>

# Apache implements `%{*}t` via `apr_strftime()`, which just calls the native
# platform's `strftime()`.

from   datetime import datetime
import re
from   .types   import FieldType, integer
from   .util    import parse_apache_timestamp

YEAR   = r'[0-9]{4,}'
MONTH  = r'(?:0[1-9]|1[012])'
MDAY   = r'(?:[ 0][1-9]|[12][0-9]|3[01])'
HOUR   = r'(?:[ 01][0-9]|2[0-3])'
HOUR12 = r'(?:[ 0][1-9]|1[0-2])'
MINUTE = r'[ 0-5][0-9]'
SECOND = r'(?:[0-5][0-9]|60)'

WEEKNUM     = r'(?:[0-4][0-9]|5[0-3])'  # 00-53
ISO_WEEKNUM = r'(?:0[1-9]|[1-4][0-9]|5[0-3])'  # 01-53

# All strftime converters must pass `None` through unmodified in order to
# handle directives like `%200{%Y-%m-%d}t` matching "-".

word = FieldType(r'\w+', lambda s: None if s is None else s)

def none_int(s):
    return None if s is None else int(s)

none_integer = integer._replace(converter=none_int)

STRFTIME_DIRECTIVES = {
    '%': (None, FieldType('%', None)),
    'a': ('abbrev_wday', word),
    'A': ('full_wday', word),
    'b': ('abbrev_mon', word),
    'B': ('full_mon', word),
    'C': ('century', FieldType(r'[0-9]{2,}', none_int)),
    'd': ('mday', FieldType(MDAY, none_int)),
    'D': (
        'date',
        FieldType(
            '{}/{}/[0-9][0-9]'.format(MONTH, MDAY),
            lambda s: datetime.strptime(s, '%m/%d/%y').date() if s is not None else None,
        )
    ),
    'e': ('mday', FieldType(MDAY, none_int)),
    'F': (
        'date',
        FieldType(
            '{}-{}-{}'.format(YEAR, MONTH, MDAY),
            lambda s: datetime.strptime(s, '%Y-%m-%d').date() if s is not None else None,
        )
    ),
    'g': ('abbrev_week_year', FieldType(r'[0-9][0-9]', none_int)),
    'G': ('week_year', FieldType(YEAR, none_int)),
    'h': ('abbrev_mon', word),
    'H': ('hour', FieldType(HOUR, none_int)),
    'I': ('hour12', FieldType(HOUR12, none_int)),
    'j': (
        'yday',
        FieldType(
            # 001−366:
            '0(?:0[1-9]|[1-9][0-9])|[12][0-9][0-9]|3(?:[0-5][0-9]|6[0-6])',
            none_int
        )
    ),
    'm': ('mon', FieldType(MONTH, none_int)),
    'M': ('min', FieldType(MINUTE, none_int)),
    'n': (None, FieldType('\n', None)),
    'p': ('am_pm', word),
    'R': (
        'hour_min',
        FieldType(
            '{}:{}'.format(HOUR, MINUTE),
            lambda s: datetime.strptime(s, '%H:%M').time() if s is not None else None,
        )
    ),
    's': ('epoch', none_integer),
    'S': ('sec', FieldType(SECOND, none_int)),
    't': (None, FieldType('\t', None)),
    'T': (
        'time',
        FieldType(
            '{}:{}:{}'.format(HOUR, MINUTE, SECOND),
            lambda s: datetime.strptime(s, '%H:%M:%S').time() if s is not None else None,
        )
    ),
    'u': ('iso_wday', FieldType(r'[1-7]', none_int)),
    'U': ('sunday_weeknum', FieldType(WEEKNUM, none_int)),
    'V': ('iso_weeknum', FieldType(ISO_WEEKNUM, none_int)),
    'w': ('wday', FieldType(r'[0-6]', none_int)),
    'W': ('monday_weeknum', FieldType(WEEKNUM, none_int)),
    'y': ('abbrev_year', FieldType(r'[0-9][0-9]', none_int)),
    'Y': ('year', FieldType(YEAR, none_int)),
    'z': (
        'timezone',
        FieldType(
            ### TODO: Get rid of the `?` here?
            r'(?:[-+](?:[01][0-9]|2[0-3])[0-5][0-9])?',
            lambda s: datetime.strptime(s, '%z').tzinfo if s else None,
        )
    ),
    'Z': ('tzname', word),

#    'c':  # C locale: %a %b %e %T %Y
#    'r':  # C locale: %I:%M:%S %p
#    'x':  # C locale: %m/%d/%y
#    'X':  # C locale: %T

#    'E*', 'O*': No.
}

SPECIAL_PARAMETERS = {
    '': ('timestamp', FieldType(r'\[[^]]+\]', parse_apache_timestamp)),
    'sec': ('epoch', none_integer),
    'msec': ('milliepoch', none_integer),
    'usec': ('microepoch', none_integer),
    'msec_frac': ('msec_frac', FieldType(r'[0-9]{3}', none_int)),
    'usec_frac': ('usec_frac', FieldType(r'[0-9]{6}', none_int)),
}

def strftime2regex(param):
    m = re.match(r'^(begin|end)(?::|\Z)', param)
    if m:
        param = param[m.end():]
        prefix = m.group(1) + '_'
        modifier = m.group(0)
    else:
        prefix = ''
        modifier = ''
    if param in SPECIAL_PARAMETERS:
        name, dtype = SPECIAL_PARAMETERS[param]
        return (
            [(
                (prefix + 'request_time_fields', name),
                modifier + param,
                dtype.converter,
            )],
            r'({})'.format(dtype.regex),
        )
    else:
        from .directives import format2regex
        groups, rgx = format2regex(param, STRFTIME_DIRECTIVES, {}, simple=True)
        groups = [
            (
                (prefix + 'request_time_fields', name),
                modifier + directive,
                converter,
            ) for (name, directive, converter) in groups
        ]
        return (groups, rgx)
