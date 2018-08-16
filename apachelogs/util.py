from   datetime import datetime, timedelta, timezone
import re

TIME_FIELD_TOKEN = 'TIME_FIELD'

CLF_NULL_TOKEN = object()

MONTH_SNAMES = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
]

APACHE_TS_RGX = re.compile(r'''
    ^\[?
    (?P<day>\d\d)   / (?P<month>\w\w\w) / (?P<year>\d{4,})
    :(?P<hour>\d\d) : (?P<minute>\d\d)  : (?P<second>\d\d)
    \s* (?P<tzoffset_sign>[-+]) (?P<tzoffset_hour>\d\d) (?P<tzoffset_min>\d\d)
    \]?$
''', flags=re.X)

def parse_apache_timestamp(s):
    # This fails when in a locale with different month snames:
    #return datetime.strptime(s.strip('[]'), '%d/%b/%Y:%H:%M:%S %z')
    m = APACHE_TS_RGX.match(s)
    if not m:
        raise ValueError(s)
    data = m.groupdict()
    for k in 'year day hour minute second'.split():
        data[k] = int(data[k])
    data['month'] = MONTH_SNAMES.index(data['month']) + 1
    tzoffset = timedelta(
        hours   = int(data.pop('tzoffset_hour')),
        minutes = int(data.pop('tzoffset_min')),
    )
    if data.pop('tzoffset_sign') == '-':
        tzoffset *= -1
    data['tzinfo'] = timezone(tzoffset)
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

def assemble_datetime(fields):
    if "apache_timestamp" in fields:
        return parse_apache_timestamp(fields["apache_timestamp"])
    elif "unix" in fields:
        return datetime.fromtimestamp(
            fields["unix"],
            fields.get("timezone") or timezone.utc,
            # fields["timezone"] may be None, in which case we still want the
            # timezone to be UTC
        )
    else:
        try:
            ### TODO: Use yday, date, time, and hour_min fields when necessary
            ### TODO: Use word fields when necessary
            return datetime(
                year   = fields["year"],
                month  = fields["mon"],
                day    = fields["mday"],
                hour   = fields["hour"],
                minute = fields["min"],
                second = fields["sec"],
                tzinfo = fields.get("timezone"),
            )
        except KeyError:
            return None
