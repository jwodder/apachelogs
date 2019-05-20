from   datetime   import date, datetime, time, timedelta, timezone
import locale
import pytest
from   apachelogs import LogParser

w5 = timezone(timedelta(hours=-5))
w4 = timezone(timedelta(hours=-4))

@pytest.mark.parametrize('fmt,entry,fields', [
    (
        '%{%a %b %d}t %r',
        'Sat Nov 25 GET / HTTP/1.1',
        {
            "request_line": "GET / HTTP/1.1",
            "request_time": None,
            "request_time_fields": {
                "abbrev_wday": "Sat",
                "abbrev_mon": "Nov",
                "mday": 25,
            },
            "directives": {
                "%{%a}t": "Sat",
                "%{%b}t": "Nov",
                "%{%d}t": 25,
                "%r": "GET / HTTP/1.1",
            },
        },
    ),

    (
        '%{%A %B %d}t %r',
        'Saturday November 25 GET / HTTP/1.1',
        {
            "request_line": "GET / HTTP/1.1",
            "request_time": None,
            "request_time_fields": {
                "full_wday": "Saturday",
                "full_mon": "November",
                "mday": 25,
            },
            "directives": {
                "%{%A}t": "Saturday",
                "%{%B}t": "November",
                "%{%d}t": 25,
                "%r": "GET / HTTP/1.1",
            },
        },
    ),

    (
        '%{%w (%u) %m/%d}t %r',
        '6 (6) 11/25 GET / HTTP/1.1',
        {
            "request_line": "GET / HTTP/1.1",
            "request_time": None,
            "request_time_fields": {
                "wday": 6,
                "iso_wday": 6,
                "mon": 11,
                "mday": 25,
            },
            "directives": {
                "%{%w}t": 6,
                "%{%u}t": 6,
                "%{%m}t": 11,
                "%{%d}t": 25,
                "%r": "GET / HTTP/1.1",
            },
        },
    ),

    (
        '%{%s}t %r',
        '1511642826 GET / HTTP/1.1',
        {
            "request_line": "GET / HTTP/1.1",
            "request_time": datetime(2017, 11, 25, 20, 47, 6, tzinfo=timezone.utc),
            "request_time_fields": {"epoch": 1511642826},
            "directives": {
                "%{%s}t": 1511642826,
                "%r": "GET / HTTP/1.1",
            },
        },
    ),

    (
        '%{%s@%z}t %r',
        '1511642826@-0500 GET / HTTP/1.1',
        {
            "request_line": "GET / HTTP/1.1",
            "request_time": datetime(2017, 11, 25, 15, 47, 6, tzinfo=w5),
            "request_time_fields": {"epoch": 1511642826, "timezone": w5},
            "directives": {
                "%{%s}t": 1511642826,
                "%{%z}t": w5,
                "%r": "GET / HTTP/1.1",
            },
        },
    ),

    (
        '%{%Y-%m-%d %H:%M:%S}t %r',
        '2017-11-25 20:47:06 GET / HTTP/1.1',
        {
            "request_line": "GET / HTTP/1.1",
            "request_time": datetime(2017, 11, 25, 20, 47, 6),
            "request_time_fields": {
                "year": 2017,
                "mon": 11,
                "mday": 25,
                "hour": 20,
                "min": 47,
                "sec": 6,
            },
            "directives": {
                "%{%Y}t": 2017,
                "%{%m}t": 11,
                "%{%d}t": 25,
                "%{%H}t": 20,
                "%{%M}t": 47,
                "%{%S}t": 6,
                "%r": "GET / HTTP/1.1",
            },
        },
    ),

    (
        '%{%Y-%m-%d %H:%M:%S %z}t %r',
        '2017-11-25 20:47:06 -0500 GET / HTTP/1.1',
        {
            "request_line": "GET / HTTP/1.1",
            "request_time": datetime(2017, 11, 25, 20, 47, 6, tzinfo=w5),
            "request_time_fields": {
                "year": 2017,
                "mon": 11,
                "mday": 25,
                "hour": 20,
                "min": 47,
                "sec": 6,
                "timezone": w5,
            },
            "directives": {
                "%{%Y}t": 2017,
                "%{%m}t": 11,
                "%{%d}t": 25,
                "%{%H}t": 20,
                "%{%M}t": 47,
                "%{%S}t": 6,
                "%{%z}t": w5,
                "%r": "GET / HTTP/1.1",
            },
        },
    ),

    (
        '%{%s}t@%{%z}t %r',
        '1511642826@-0500 GET / HTTP/1.1',
        {
            "request_line": "GET / HTTP/1.1",
            "request_time": datetime(2017, 11, 25, 15, 47, 6, tzinfo=w5),
            "request_time_fields": {"epoch": 1511642826, "timezone": w5},
            "directives": {
                "%{%s}t": 1511642826,
                "%{%z}t": w5,
                "%r": "GET / HTTP/1.1",
            },
        },
    ),

    (
        '%{%Y-%m-%d}t %{%H:%M:%S}t %r',
        '2017-11-25 20:47:06 GET / HTTP/1.1',
        {
            "request_line": "GET / HTTP/1.1",
            "request_time": datetime(2017, 11, 25, 20, 47, 6),
            "request_time_fields": {
                "year": 2017,
                "mon": 11,
                "mday": 25,
                "hour": 20,
                "min": 47,
                "sec": 6,
            },
            "directives": {
                "%{%Y}t": 2017,
                "%{%m}t": 11,
                "%{%d}t": 25,
                "%{%H}t": 20,
                "%{%M}t": 47,
                "%{%S}t": 6,
                "%r": "GET / HTTP/1.1",
            },
        },
    ),

    (
        '%{%Y-%m-%d}t %{%H:%M:%S}t %{%z}t %r',
        '2017-11-25 20:47:06 -0500 GET / HTTP/1.1',
        {
            "request_line": "GET / HTTP/1.1",
            "request_time": datetime(2017, 11, 25, 20, 47, 6, tzinfo=w5),
            "request_time_fields": {
                "year": 2017,
                "mon": 11,
                "mday": 25,
                "hour": 20,
                "min": 47,
                "sec": 6,
                "timezone": w5,
            },
            "directives": {
                "%{%Y}t": 2017,
                "%{%m}t": 11,
                "%{%d}t": 25,
                "%{%H}t": 20,
                "%{%M}t": 47,
                "%{%S}t": 6,
                "%{%z}t": w5,
                "%r": "GET / HTTP/1.1",
            },
        },
    ),

    (
        "%{%D %T}t",
        "05/06/19 13:42:26",
        {
            "request_time": datetime(2019, 5, 6, 13, 42, 26),
            "request_time_fields": {
                "date": date(2019, 5, 6),
                "time": time(13, 42, 26),
            },
            "directives": {
                "%{%D}t": date(2019, 5, 6),
                "%{%T}t": time(13, 42, 26),
            },
        },
    ),

    (
        "%{%D%%%T}t",
        "05/06/19%13:42:26",
        {
            "request_time": datetime(2019, 5, 6, 13, 42, 26),
            "request_time_fields": {
                "date": date(2019, 5, 6),
                "time": time(13, 42, 26),
            },
            "directives": {
                "%{%D}t": date(2019, 5, 6),
                "%{%T}t": time(13, 42, 26),
            },
        },
    ),

    (
        "%{%D%t%T}t",
        "05/06/19\t13:42:26",
        {
            "request_time": datetime(2019, 5, 6, 13, 42, 26),
            "request_time_fields": {
                "date": date(2019, 5, 6),
                "time": time(13, 42, 26),
            },
            "directives": {
                "%{%D}t": date(2019, 5, 6),
                "%{%T}t": time(13, 42, 26),
            },
        },
    ),

    (
        "%{%F %R:%S}t",
        "2019-05-06 13:42:26",
        {
            "request_time": datetime(2019, 5, 6, 13, 42, 26),
            "request_time_fields": {
                "date": date(2019, 5, 6),
                "hour_min": time(13, 42),
                "sec": 26,
            },
            "directives": {
                "%{%F}t": date(2019, 5, 6),
                "%{%R}t": time(13, 42),
                "%{%S}t": 26,
            },
        },
    ),

    (
        "%{begin:%F %R:%S}t",
        "2019-05-06 13:42:26",
        {
            "begin_request_time": datetime(2019, 5, 6, 13, 42, 26),
            "begin_request_time_fields": {
                "date": date(2019, 5, 6),
                "hour_min": time(13, 42),
                "sec": 26,
            },
            "directives": {
                "%{begin:%F}t": date(2019, 5, 6),
                "%{begin:%R}t": time(13, 42),
                "%{begin:%S}t": 26,
            },
        },
    ),

    (
        "%{end:%F %R:%S}t",
        "2019-05-06 13:42:26",
        {
            "end_request_time": datetime(2019, 5, 6, 13, 42, 26),
            "end_request_time_fields": {
                "date": date(2019, 5, 6),
                "hour_min": time(13, 42),
                "sec": 26,
            },
            "directives": {
                "%{end:%F}t": date(2019, 5, 6),
                "%{end:%R}t": time(13, 42),
                "%{end:%S}t": 26,
            },
        },
    ),

    (
        "%<{end:%F %R:%S}t",
        "2019-05-06 13:42:26",
        {
            "original_end_request_time": datetime(2019, 5, 6, 13, 42, 26),
            "original_end_request_time_fields": {
                "date": date(2019, 5, 6),
                "hour_min": time(13, 42),
                "sec": 26,
            },
            "directives": {
                "%<{end:%F}t": date(2019, 5, 6),
                "%<{end:%R}t": time(13, 42),
                "%<{end:%S}t": 26,
            },
        },
    ),

    (
        "%{}t",
        '[05/Nov/2017:02:01:01 -0500]',
        {
            "request_time": datetime(2017,11, 5, 2, 1, 1, tzinfo=w5),
            "request_time_fields": {
                "timestamp": datetime(2017,11, 5, 2, 1, 1, tzinfo=w5),
            },
            "directives": {
                "%{}t": datetime(2017,11, 5, 2, 1, 1, tzinfo=w5),
            },
        }
    ),

    (
        "%{begin}t",
        '[05/Nov/2017:02:01:01 -0500]',
        {
            "begin_request_time": datetime(2017,11, 5, 2, 1, 1, tzinfo=w5),
            "begin_request_time_fields": {
                "timestamp": datetime(2017,11, 5, 2, 1, 1, tzinfo=w5),
            },
            "directives": {
                "%{begin}t": datetime(2017,11, 5, 2, 1, 1, tzinfo=w5),
            },
        }
    ),

    (
        "%{end}t",
        '[05/Nov/2017:02:01:01 -0500]',
        {
            "end_request_time": datetime(2017,11, 5, 2, 1, 1, tzinfo=w5),
            "end_request_time_fields": {
                "timestamp": datetime(2017,11, 5, 2, 1, 1, tzinfo=w5),
            },
            "directives": {
                "%{end}t": datetime(2017,11, 5, 2, 1, 1, tzinfo=w5),
            },
        }
    ),

    (
        "%{begin:}t",
        '[05/Nov/2017:02:01:01 -0500]',
        {
            "begin_request_time": datetime(2017,11, 5, 2, 1, 1, tzinfo=w5),
            "begin_request_time_fields": {
                "timestamp": datetime(2017,11, 5, 2, 1, 1, tzinfo=w5),
            },
            "directives": {
                "%{begin:}t": datetime(2017,11, 5, 2, 1, 1, tzinfo=w5),
            },
        }
    ),

    (
        "%{end:}t",
        '[05/Nov/2017:02:01:01 -0500]',
        {
            "end_request_time": datetime(2017,11, 5, 2, 1, 1, tzinfo=w5),
            "end_request_time_fields": {
                "timestamp": datetime(2017,11, 5, 2, 1, 1, tzinfo=w5),
            },
            "directives": {
                "%{end:}t": datetime(2017,11, 5, 2, 1, 1, tzinfo=w5),
            },
        }
    ),

    (
        '%{%Y%n%m%t%d}t',
        '2019 05 19',
        {
            "request_time": None,
            "request_time_fields": {
                "year": 2019,
                "mon": 5,
                "mday": 19,
            },
            "directives": {
                "%{%Y}t": 2019,
                "%{%m}t": 5,
                "%{%d}t": 19,
            },
        },
    ),

    (
        '%{%Y%n%m%t%d}t',
        '2019 \t 05 \n 19',
        {
            "request_time": None,
            "request_time_fields": {
                "year": 2019,
                "mon": 5,
                "mday": 19,
            },
            "directives": {
                "%{%Y}t": 2019,
                "%{%m}t": 5,
                "%{%d}t": 19,
            },
        },
    ),

    (
        '%{%Y%n%m%t%d}t',
        '20190519',
        {
            "request_time": None,
            "request_time_fields": {
                "year": 2019,
                "mon": 5,
                "mday": 19,
            },
            "directives": {
                "%{%Y}t": 2019,
                "%{%m}t": 5,
                "%{%d}t": 19,
            },
        },
    ),

    (
        '%200{%I:%M:%S %p}t',
        '12:34:56 ',
        {
            "request_time": None,
            "request_time_fields": {
                "hour12": 12,
                "min": 34,
                "sec": 56,
                "am_pm": "",
            },
            "directives": {
                "%200{%I}t": 12,
                "%200{%M}t": 34,
                "%200{%S}t": 56,
                "%200{%p}t": "",
            },
        },
    ),

    (
        '%200{%I:%M:%S %p}t',
        '-',
        {
            "request_time": None,
            "request_time_fields": {
                "hour12": None,
                "min": None,
                "sec": None,
                "am_pm": None,
            },
            "directives": {
                "%200{%I}t": None,
                "%200{%M}t": None,
                "%200{%S}t": None,
                "%200{%p}t": None,
            },
        },
    ),

    (
        '%{%s %Z}t',
        '1511642826 GMT',
        {
            "request_time": datetime(2017, 11, 25, 20, 47, 6, tzinfo=timezone.utc),
            "request_time_fields": {
                "epoch": 1511642826,
                "tzname": "GMT",
            },
            "directives": {
                "%{%s}t": 1511642826,
                "%{%Z}t": "GMT",
            },
        },
    ),

    (
        '%{%s %Z}t',
        '1511642826 UTC',
        {
            "request_time": datetime(2017, 11, 25, 20, 47, 6, tzinfo=timezone.utc),
            "request_time_fields": {
                "epoch": 1511642826,
                "tzname": "UTC",
            },
            "directives": {
                "%{%s}t": 1511642826,
                "%{%Z}t": "UTC",
            },
        },
    ),

    (
        '%{%s %Z}t',
        '1511642826 EST',
        {
            "request_time": datetime(2017, 11, 25, 15, 47, 6, tzinfo=w5),
            "request_time_fields": {
                "epoch": 1511642826,
                "tzname": "EST",
            },
            "directives": {
                "%{%s}t": 1511642826,
                "%{%Z}t": "EST",
            },
        },
    ),

    (
        '%{%s %Z}t',
        '1558378254 EDT',
        {
            "request_time": datetime(2019, 5, 20, 14, 50, 54, tzinfo=w4),
            "request_time_fields": {
                "epoch": 1558378254,
                "tzname": "EDT",
            },
            "directives": {
                "%{%s}t": 1558378254,
                "%{%Z}t": "EDT",
            },
        },
    ),

    (
        '%{%s %Z}t',
        '1558378254 XXX',
        {
            "request_time": datetime(2019, 5, 20, 18, 50, 54, tzinfo=timezone.utc),
            "request_time_fields": {
                "epoch": 1558378254,
                "tzname": "XXX",
            },
            "directives": {
                "%{%s}t": 1558378254,
                "%{%Z}t": "XXX",
            },
        },
    ),

    (
        '%{%FT%T %Z}t',
        '2019-02-20T14:54:43 GMT',
        {
            "request_time": datetime(2019, 2, 20, 14, 54, 43, tzinfo=timezone.utc),
            "request_time_fields": {
                "date": date(2019, 2, 20),
                "time": time(14, 54, 43),
                "tzname": "GMT",
            },
            "directives": {
                "%{%F}t": date(2019, 2, 20),
                "%{%T}t": time(14, 54, 43),
                "%{%Z}t": "GMT",
            },
        },
    ),

    (
        '%{%FT%T %Z}t',
        '2019-02-20T14:54:43 UTC',
        {
            "request_time": datetime(2019, 2, 20, 14, 54, 43, tzinfo=timezone.utc),
            "request_time_fields": {
                "date": date(2019, 2, 20),
                "time": time(14, 54, 43),
                "tzname": "UTC",
            },
            "directives": {
                "%{%F}t": date(2019, 2, 20),
                "%{%T}t": time(14, 54, 43),
                "%{%Z}t": "UTC",
            },
        },
    ),

    (
        '%{%FT%T %Z}t',
        '2019-02-20T14:54:43 EST',
        {
            "request_time": datetime(2019, 2, 20, 14, 54, 43, tzinfo=w5),
            "request_time_fields": {
                "date": date(2019, 2, 20),
                "time": time(14, 54, 43),
                "tzname": "EST",
            },
            "directives": {
                "%{%F}t": date(2019, 2, 20),
                "%{%T}t": time(14, 54, 43),
                "%{%Z}t": "EST",
            },
        },
    ),

    (
        '%{%FT%T %Z}t',
        '2019-05-20T14:54:43 EDT',
        {
            "request_time": datetime(2019, 5, 20, 14, 54, 43, tzinfo=w4),
            "request_time_fields": {
                "date": date(2019, 5, 20),
                "time": time(14, 54, 43),
                "tzname": "EDT",
            },
            "directives": {
                "%{%F}t": date(2019, 5, 20),
                "%{%T}t": time(14, 54, 43),
                "%{%Z}t": "EDT",
            },
        },
    ),

    (
        '%{%FT%T %Z}t',
        '2019-05-20T14:54:43 XXX',
        {
            "request_time": datetime(2019, 5, 20, 14, 54, 43),
            "request_time_fields": {
                "date": date(2019, 5, 20),
                "time": time(14, 54, 43),
                "tzname": "XXX",
            },
            "directives": {
                "%{%F}t": date(2019, 5, 20),
                "%{%T}t": time(14, 54, 43),
                "%{%Z}t": "XXX",
            },
        },
    ),
])
def test_parse_custom_time(fmt, entry, fields):
    log_entry = LogParser(fmt, encoding='utf-8').parse(entry)
    for k,v in fields.items():
        assert getattr(log_entry, k) == v

@pytest.mark.parametrize('fmt,entry,fields', [
    (
        '%{%d %b %Y %H:%M:%S %z}t',
        '19 Mär 2019 01:39:12 +0000',
        {
            "request_time": datetime(2019, 3, 19, 1, 39, 12, tzinfo=timezone.utc),
            "request_time_fields": {
                "mday": 19,
                "abbrev_mon": "Mär",
                "year": 2019,
                "hour": 1,
                "min": 39,
                "sec": 12,
                "timezone": timezone.utc,
            },
            "directives": {
                "%{%d}t": 19,
                "%{%b}t": "Mär",
                "%{%Y}t": 2019,
                "%{%H}t": 1,
                "%{%M}t": 39,
                "%{%S}t": 12,
                "%{%z}t": timezone.utc,
            },
        },
    ),

    (
        '%{%d %B %Y %H:%M:%S %z}t',
        '19 März 2019 01:39:12 +0000',
        {
            "request_time": datetime(2019, 3, 19, 1, 39, 12, tzinfo=timezone.utc),
            "request_time_fields": {
                "mday": 19,
                "full_mon": "März",
                "year": 2019,
                "hour": 1,
                "min": 39,
                "sec": 12,
                "timezone": timezone.utc,
            },
            "directives": {
                "%{%d}t": 19,
                "%{%B}t": "März",
                "%{%Y}t": 2019,
                "%{%H}t": 1,
                "%{%M}t": 39,
                "%{%S}t": 12,
                "%{%z}t": timezone.utc,
            },
        },
    ),

    (
        '%{%G--%V %a %H:%M:%S}t',
        '2019--20 So 12:34:56',
        {
            "request_time": datetime(2019, 5, 19, 12, 34, 56),
            "request_time_fields": {
                "iso_year": 2019,
                "iso_weeknum": 20,
                "abbrev_wday": "So",
                "hour": 12,
                "min": 34,
                "sec": 56,
            },
            "directives": {
                "%{%G}t": 2019,
                "%{%V}t": 20,
                "%{%a}t": "So",
                "%{%H}t": 12,
                "%{%M}t": 34,
                "%{%S}t": 56,
            },
        },
    ),

    (
        '%{%G--%V %A %H:%M:%S}t',
        '2019--20 Sonntag 12:34:56',
        {
            "request_time": datetime(2019, 5, 19, 12, 34, 56),
            "request_time_fields": {
                "iso_year": 2019,
                "iso_weeknum": 20,
                "full_wday": "Sonntag",
                "hour": 12,
                "min": 34,
                "sec": 56,
            },
            "directives": {
                "%{%G}t": 2019,
                "%{%V}t": 20,
                "%{%A}t": "Sonntag",
                "%{%H}t": 12,
                "%{%M}t": 34,
                "%{%S}t": 56,
            },
        },
    ),
])
def test_parse_custom_german_time(fmt, entry, fields):
    oldlocale = locale.setlocale(locale.LC_ALL)
    try:
        locale.setlocale(locale.LC_ALL, 'de_DE.utf8')
    except locale.Error:
        pytest.skip('Locale not supported')
    else:
        entry = LogParser(fmt).parse(entry)
        for k,v in fields.items():
            assert getattr(entry, k) == v
    finally:
        locale.setlocale(locale.LC_ALL, oldlocale)
