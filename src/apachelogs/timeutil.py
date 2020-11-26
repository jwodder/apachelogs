import calendar
from   datetime import date, datetime, timedelta, timezone
import re
import time

#: The names of the months in English
MONTH_FULL_NAMES = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12,
}

#: The abbreviated names of the months in English
MONTH_SNAMES = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12,
}

#: The names of the days of the week in English
WDAY_FULL_NAMES = {
    "Monday": 1,
    "Tuesday": 2,
    "Wednesday": 3,
    "Thursday": 4,
    "Friday": 5,
    "Saturday": 6,
    "Sunday": 7,
}

#: The abbreviated names of the days of the week in English
WDAY_SNAMES = {
    "Mon": 1,
    "Tue": 2,
    "Wed": 3,
    "Thu": 4,
    "Fri": 5,
    "Sat": 6,
    "Sun": 7,
}

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
        data['month'] = MONTH_SNAMES[data['month']]
    except KeyError:
        raise ValueError(s)
    tzoffset = timedelta(
        hours   = int(data.pop('tzoffset_hour')),
        minutes = int(data.pop('tzoffset_min')),
    )
    if data.pop('tzoffset_sign') == '-':
        tzoffset *= -1
    data['tzinfo'] = timezone(tzoffset)
    return datetime(**data)

def assemble_datetime(fields):
    """
    Given a `dict` of time fields, return a `datetime.datetime` object if there
    is enough information to create one, `None` otherwise.
    """
    if fields.get("timezone") is not None:
        tz = fields["timezone"]
    elif fields.get("tzname") is not None:
        if fields["tzname"] in ('GMT', 'UTC'):
            tz = timezone.utc
        elif fields["tzname"] == time.tzname[0]:
            tz = timezone(timedelta(seconds=-time.timezone))
        elif time.daylight and fields["tzname"] == time.tzname[1]:
            tz = timezone(timedelta(seconds=-time.altzone))
        else:
            tz = None
    else:
        tz = None

    if fields.get("timestamp") is not None:
        return fields["timestamp"]
    elif fields.get("microepoch") is not None:
        return datetime.fromtimestamp(
            fields["microepoch"] / 1000000,
            tz or timezone.utc,
        )
    elif fields.get("milliepoch") is not None:
        return datetime.fromtimestamp(
            fields["milliepoch"] / 1000,
            tz or timezone.utc,
        )
    elif fields.get("epoch") is not None:
        return datetime.fromtimestamp(fields["epoch"], tz or timezone.utc)
    else:
        locale_wday_names = {
            w:i for i,w in enumerate(calendar.day_name, start=1)
        }
        locale_wday_abbrevs = {
            w:i for i,w in enumerate(calendar.day_abbr, start=1)
        }

        if fields.get("iso_wday") is not None:
            iso_wday = fields["iso_wday"]
        elif fields.get("wday") is not None:
            iso_wday = fields["wday"] or 7
        elif fields.get("full_wday") is not None \
                and fields["full_wday"] in WDAY_FULL_NAMES:
            iso_wday = WDAY_FULL_NAMES[fields["full_wday"]]
        elif fields.get("full_wday") is not None \
                and fields["full_wday"] in locale_wday_names:
            iso_wday = locale_wday_names[fields["full_wday"]]
        elif fields.get("abbrev_wday") is not None \
                and fields["abbrev_wday"] in WDAY_SNAMES:
            iso_wday = WDAY_SNAMES[fields["abbrev_wday"]]
        elif fields.get("abbrev_wday") is not None \
                and fields["abbrev_wday"] in locale_wday_abbrevs:
            iso_wday = locale_wday_abbrevs[fields["abbrev_wday"]]
        else:
            iso_wday = None

        thedate = None

        if fields.get("year") is not None:
            year = fields["year"]
        elif fields.get("date") is not None:
            year = fields["date"].year
        elif fields.get("abbrev_year") is not None:
            if fields.get("century") is not None:
                year = fields["century"] * 100 + fields["abbrev_year"]
            elif fields["abbrev_year"] < 69:
                year = 2000 + fields["abbrev_year"]
            else:
                year = 1900 + fields["abbrev_year"]
        elif fields.get("iso_year") is not None \
                and fields.get("iso_weeknum") is not None \
                and iso_wday is not None:
            thedate = fromisocalendar(
                fields["iso_year"],
                fields["iso_weeknum"],
                iso_wday,
            )
            year = thedate.year
        elif fields.get("abbrev_iso_year") is not None \
                and fields.get("iso_weeknum") is not None \
                and iso_wday is not None:
            iso_year = fields["abbrev_iso_year"]
            iso_year += 2000 if iso_year < 69 else 1900
            thedate = fromisocalendar(iso_year, fields["iso_weeknum"], iso_wday)
            year = thedate.year
        else:
            return None

        locale_month_names = {
            m:i for i,m in enumerate(calendar.month_name) if i != 0
        }
        locale_month_abbrevs = {
            m:i for i,m in enumerate(calendar.month_abbr) if i != 0
        }

        if thedate is None:
            if fields.get("date") is not None:
                thedate = fields["date"]
            elif fields.get("yday") is not None:
                thedate = date(year, 1, 1) + timedelta(days=fields["yday"]-1)
            elif fields.get("sunday_weeknum") is not None \
                    and iso_wday is not None:
                thedate = datetime.strptime(
                    f'{year} {fields["sunday_weeknum"]} {iso_wday % 7}',
                    '%Y %U %w',
                ).date()
            elif fields.get("monday_weeknum") is not None \
                    and iso_wday is not None:
                thedate = datetime.strptime(
                    f'{year} {fields["monday_weeknum"]} {iso_wday % 7}',
                    '%Y %W %w',
                ).date()

        if fields.get("mon") is not None:
            month = fields["mon"]
        elif thedate is not None:
            month = thedate.month
        elif fields.get("full_mon") in MONTH_FULL_NAMES:
            month = MONTH_FULL_NAMES[fields["full_mon"]]
        elif fields.get("full_mon") in locale_month_names:
            month = locale_month_names[fields["full_mon"]]
        elif fields.get("abbrev_mon") in MONTH_SNAMES:
            month = MONTH_SNAMES[fields["abbrev_mon"]]
        elif fields.get("abbrev_mon") in locale_month_abbrevs:
            month = locale_month_abbrevs[fields["abbrev_mon"]]
        else:
            return None

        if fields.get("mday") is not None:
            day = fields["mday"]
        elif thedate is not None:
            day = thedate.day
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
            tzinfo = tz,
        )

def fromisocalendar(iso_year, iso_weeknum, iso_wday):
    """
    Convert an ISO year, ISO week number, and ISO weekday to a `datetime.date`.
    This is the inverse of `datetime.date.isocalendar()`.

    >>> fromisocalendar(2004, 1, 1)
    datetime.date(2003, 12, 29)
    >>> fromisocalendar(2004, 1, 7)
    datetime.date(2004, 1, 4)
    """

    # Python 3.8+:
    # date.fromisocalendar(iso_year, iso_weeknum, iso_wday)

    return datetime.strptime(
        f'{iso_year} {iso_weeknum} {iso_wday}',
        '%G %V %u',
    ).date()
