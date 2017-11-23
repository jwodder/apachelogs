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

def unescape(s):
    # Escape sequences used by Apache: \b \n \r \t \v \\ \" \xHH
    # cf. ap_escape_logitem() in server/util.c
    return re.sub(r'\\(x[0-9A-Fa-f]{2}|.)', _unesc, s).encode('iso-8859-1')

_unescapes = {
    't': '\t',
    'n': '\n',
    'r': '\r',
    'b': '\b',
    'v': '\v',
    # Not emitted by Apache (as of v2.4), but other servers might use it:
    'f': '\f',
}

def _unesc(m):
    esc = m.group(1)
    if esc[0] == 'x':
        return chr(int(esc[1:], 16))
    else:
        return _unescapes.get(esc, '\\' + esc)
