from   datetime    import datetime
import re
from   dateutil.tz import tzoffset

MONTH_SNAMES = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
]

APACHE_TS_RGX = re.compile(r'''
    ^\[?
    (?P<day>\d\d)   / (?P<month>\w\w\w) / (?P<year>\d{4,})
    :(?P<hour>\d\d) : (?P<minute>\d\d)  : (?P<second>\d\d)
    \s* (?P<tzoffset_sign>[-+]) (?P<tzoffset_hour>\d\d+) (?P<tzoffset_min>\d\d)
    \]?$
''', flags=re.X)

def parse_apache_timestamp(s):
    m = APACHE_TS_RGX.match(s)
    if not m:
        raise ValueError(s)
    data = m.groupdict()
    for k in 'year day hour minute second'.split():
        data[k] = int(data[k])
    data['month'] = MONTH_SNAMES.index(data['month']) + 1
    tzoffset_hour = int(data.pop('tzoffset_hour'))
    tzoffset_min  = int(data.pop('tzoffset_min'))
    offset = tzoffset_hour * 3600 + tzoffset_min * 60
    if data.pop('tzoffset_sign') == '-':
        offset *= -1
    data['tzinfo'] = tzoffset(None, offset)
    return datetime(**data)
