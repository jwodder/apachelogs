from   datetime import datetime, timedelta, timezone
import re

#: The abbreviated names of the months in English
MONTH_SNAMES = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
]

#: Compiled regex for an Apache timestamp
APACHE_TS_RGX = re.compile(r'''
    ^\[?
    (?P<day>\d\d)   / (?P<month>\w\w\w) / (?P<year>\d{4,})
    :(?P<hour>\d\d) : (?P<minute>\d\d)  : (?P<second>\d\d)
    \s* (?P<tzoffset_sign>[-+]) (?P<tzoffset_hour>\d\d) (?P<tzoffset_min>\d\d)
    \]?$
''', flags=re.X)

def parse_apache_timestamp(s):
    """
    Parse an Apache timestamp into a `datetime.datetime` object.  The month
    name in the timestamp is expected to be an abbreviated English name
    regardless of the current locale.

    >>> parse_apache_timestamp('[01/Nov/2017:07:28:29 +0000]')
    datetime.datetime(2017, 11, 1, 7, 28, 29, tzinfo=datetime.timezone.utc)

    :param str s: a string of the form ``DD/Mon/YYYY:HH:MM:SS +HHMM``
        (optionally enclosed in square brackets)
    :return: an aware `datetime.datetime`
    :raises ValueError: if ``s`` is not in the expected format
    """
    # Apache timestamps always use English month abbreviations.  Thus, parsing
    # with strptime like the below will fail when in a locale with different
    # month snames:
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
    """
    Unescape the escape sequences in the string ``s``, returning a `bytes`
    string
    """
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
    """
    Given a `dict` of time fields, return a `datetime.datetime` object if there
    is enough information to create one, `None` otherwise.
    """
    if "timestamp" in fields:
        return fields["timestamp"]
    elif "epoch" in fields:
        return datetime.fromtimestamp(
            fields["epoch"],
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
