# cf. <http://pubs.opengroup.org/onlinepubs/9699919799/functions/strftime.html>

# Note that Apache implements `%{*}t` via `apr_strftime()`, so [TODO] see that
# for finer-grained information.

from datetime import datetime
from .types   import FieldType, integer

YEAR   = r'[0-9]{4,}'
MONTH  = r'(?:0[1-9]|1[012])'
MDAY   = r'(?:[ 0][1-9]|[12][0-9]|3[01])'
HOUR   = r'(?:[ 01][0-9]|2[0-3])'
HOUR12 = r'(?:[ 0][1-9]|1[0-2])'
MINUTE = r'[ 0-5][0-9]'
SECOND = r'(?:[0-5][0-9]|60)'

WEEKNUM     = r'(?:[0-4][0-9]|5[0-3])'  # 00-53
ISO_WEEKNUM = r'(?:0[1-9]|[1-4][0-9]|5[0-3])'  # 01-53

### TODO: Should this be ASCII-only?
word = FieldType(r'\w+', str)

STRFTIME_DIRECTIVES = {
    '%': (None, FieldType('%', None)),
    'a': ('abbrev_wday', word),
    'A': ('full_wday', word),
    'b': ('abbrev_mon', word),
    'B': ('full_mon', word),
    'C': ('century', FieldType(r'[0-9]{2,}', int)),
    'd': ('mday', FieldType(MDAY, int)),
    'D': (
        'date',
        FieldType(
            '{}/{}/[0-9][0-9]'.format(MONTH, MDAY),
            lambda s: datetime.strptime(s, '%m/%d/%y').date(),
        )
    ),
    'e': ('mday', FieldType(MDAY, int)),
    'F': (
        'date',
        FieldType(
            '{}-{}-{}'.format(YEAR, MONTH, MDAY),
            lambda s: datetime.strptime(s, '%Y-%m-%d').date(),
        )
    ),
    'g': ('abbrev_week_year', FieldType(r'[0-9][0-9]', int)),
    'G': ('week_year', FieldType(YEAR, int)),
    'h': ('abbrev_mon', word),
    'H': ('hour', FieldType(HOUR, int)),
    'I': ('hour12', FieldType(HOUR12, int)),
    'j': (
        'yday',
        FieldType(
            # 001−366:
            '0(?:0[1-9]|[1-9][0-9])|[12][0-9][0-9]|3(?:[0-5][0-9]|6[0-6])',
            int
        )
    ),
    'm': ('mon', FieldType(MONTH, int)),
    'M': ('min', FieldType(MINUTE, int)),
    'n': (None, FieldType('\n', None)),
    'p': ('am_pm', word),
    'R': (
        'hour_min',
        FieldType(
            '{}:{}'.format(HOUR, MINUTE),
            lambda s: datetime.strptime(s, '%H:%M').time(),
        )
    ),
    's': ('epoch', integer),
    'S': ('sec', FieldType(SECOND, int)),
    't': (None, FieldType('\t', None)),
    'T': (
        'time',
        FieldType(
            '{}:{}:{}'.format(HOUR, MINUTE, SECOND),
            lambda s: datetime.strptime(s, '%H:%M:%S').time(),
        )
    ),
    'u': ('iso_wday', FieldType(r'[1-7]', int)),
    'U': ('sunday_weeknum', FieldType(WEEKNUM, int)),
    'V': ('iso_weeknum', FieldType(ISO_WEEKNUM, int)),
    'w': ('wday', FieldType(r'[0-6]', int)),
    'W': ('monday_weeknum', FieldType(WEEKNUM, int)),
    'y': ('abbrev_year', FieldType(r'[0-9][0-9]', int)),
    'Y': ('year', FieldType(YEAR, int)),
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
    'sec': ('epoch', integer),
    'msec': ('milliepoch', integer),
    'usec': ('microepoch', integer),
    'msec_frac': ('msec_frac', integer),
    'usec_frac': ('msec_frac', integer),
}

def strftime2regex(param):
    if param in SPECIAL_PARAMETERS:
        name, dtype = SPECIAL_PARAMETERS[param]
        return [
            (('request_time_fields', name), '%{'+param+'}t', dtype.converter),
            r'({})'.format(dtype.regex),
        ]
    else:
        from .directives import format2regex
        groups, rgx = format2regex(param, STRFTIME_DIRECTIVES, {})
        groups = [
            (('request_time_fields', name), '%{' + directive + '}t', converter)
            for (name, directive, converter) in groups
        ]
        return (groups, rgx)
