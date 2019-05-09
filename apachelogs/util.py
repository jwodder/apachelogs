from   datetime import date, datetime, timedelta, timezone
import re

#: The names of the months in English
MONTH_FULL_NAMES = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December',
]

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
    if s is None:
        return None
    m = APACHE_TS_RGX.match(s)
    if not m:
        raise ValueError(s)
    data = m.groupdict()
    for k in 'year day hour minute second'.split():
        data[k] = int(data[k])
    try:
        data['month'] = MONTH_SNAMES.index(data['month']) + 1
    except ValueError:
        raise ValueError(s)
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
        return _unescapes.get(esc, esc)

def assemble_datetime(fields):
    """
    Given a `dict` of time fields, return a `datetime.datetime` object if there
    is enough information to create one, `None` otherwise.
    """
    if fields.get("timestamp") is not None:
        return fields["timestamp"]
    elif fields.get("microepoch") is not None:
        return datetime.fromtimestamp(
            fields["microepoch"] / 1000000,
            fields.get("timezone") or timezone.utc,
            # fields["timezone"] may be None, in which case we still want the
            # timezone to be UTC
        )
    elif fields.get("milliepoch") is not None:
        return datetime.fromtimestamp(
            fields["milliepoch"] / 1000,
            fields.get("timezone") or timezone.utc,
            # fields["timezone"] may be None, in which case we still want the
            # timezone to be UTC
        )
    elif fields.get("epoch") is not None:
        return datetime.fromtimestamp(
            fields["epoch"],
            fields.get("timezone") or timezone.utc,
            # fields["timezone"] may be None, in which case we still want the
            # timezone to be UTC
        )
    else:
        if fields.get("year") is not None:
            year = fields["year"]
        elif fields.get("date") is not None:
            year = fields["date"].year
        elif fields.get("century") is not None \
                and fields.get("abbrev_year") is not None:
            year = fields["century"] * 100 + fields["abbrev_year"]
        else:
            return None

        if fields.get("mon") is not None:
            month = fields["mon"]
        elif fields.get("date") is not None:
            month = fields["date"].month
        elif fields.get("yday") is not None:
            month = (date(year, 1, 1) + timedelta(days=fields["yday"]-1)).month
        elif fields.get("full_mon") in MONTH_FULL_NAMES:
            month = MONTH_FULL_NAMES.index(fields["full_mon"]) + 1
        elif fields.get("abbrev_mon") in MONTH_SNAMES:
            month = MONTH_SNAMES.index(fields["abbrev_mon"]) + 1
        else:
            return None

        if fields.get("mday") is not None:
            day = fields["mday"]
        elif fields.get("date") is not None:
            day = fields["date"].day
        elif fields.get("yday") is not None:
            day = (date(year, 1, 1) + timedelta(days=fields["yday"]-1)).day
        else:
            return None

        if fields.get("hour") is not None:
            hour = fields["hour"]
        elif fields.get("time") is not None:
            hour = fields["time"].hour
        elif fields.get("hour_min") is not None:
            hour = fields["hour_min"].hour
        elif fields.get("hour12") is not None \
                and fields.get("am_pm") is not None \
                and fields["am_pm"].upper() in ('AM', 'PM'):
            hour = fields["hour12"] % 12
            if fields["am_pm"].upper() == "PM":
                hour += 12
        else:
            return None

        if fields.get("min") is not None:
            minute = fields["min"]
        elif fields.get("time") is not None:
            minute = fields["time"].minute
        elif fields.get("hour_min") is not None:
            minute = fields["hour_min"].minute
        else:
            return None

        if fields.get("sec") is not None:
            second = fields["sec"]
        elif fields.get("time") is not None:
            second = fields["time"].second
        else:
            return None

        if fields.get("usec_frac") is not None:
            microsecond = fields["usec_frac"]
        elif fields.get("msec_frac") is not None:
            microsecond = fields["msec_frac"] * 1000
        else:
            microsecond = 0

        return datetime(
            year   = year,
            month  = month,
            day    = day,
            hour   = hour,
            minute = minute,
            second = second,
            microsecond = microsecond,
            tzinfo = fields.get("timezone"),
        )
