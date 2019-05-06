from   datetime   import date, datetime, time, timedelta, timezone
import pytest
from   apachelogs import LogParser

w5 = timezone(timedelta(hours=-5))

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
        },
    ),

    (
        '%{%s}t %r',
        '1511642826 GET / HTTP/1.1',
        {
            "request_line": "GET / HTTP/1.1",
            "request_time": datetime(2017, 11, 25, 20, 47, 6, tzinfo=timezone.utc),
            "request_time_fields": {"epoch": 1511642826},
        },
    ),

    (
        '%{%s@%z}t %r',
        '1511642826@-0500 GET / HTTP/1.1',
        {
            "request_line": "GET / HTTP/1.1",
            "request_time": datetime(2017, 11, 25, 15, 47, 6, tzinfo=w5),
            "request_time_fields": {"epoch": 1511642826, "timezone": w5},
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
        },
    ),

    (
        '%{%s}t@%{%z}t %r',
        '1511642826@-0500 GET / HTTP/1.1',
        {
            "request_line": "GET / HTTP/1.1",
            "request_time": datetime(2017, 11, 25, 15, 47, 6, tzinfo=w5),
            "request_time_fields": {"epoch": 1511642826, "timezone": w5},
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
            }
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
            }
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
            }
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
            }
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
            }
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
            }
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
            }
        },
    ),

    (
        "%{}t",
        '[05/Nov/2017:02:01:01 -0500]',
        {
            "request_time": datetime(2017,11, 5, 2, 1, 1, tzinfo=w5),
            "request_time_fields": {
                "timestamp": datetime(2017,11, 5, 2, 1, 1, tzinfo=w5),
            }
        }
    ),

    (
        "%{begin}t",
        '[05/Nov/2017:02:01:01 -0500]',
        {
            "begin_request_time": datetime(2017,11, 5, 2, 1, 1, tzinfo=w5),
            "begin_request_time_fields": {
                "timestamp": datetime(2017,11, 5, 2, 1, 1, tzinfo=w5),
            }
        }
    ),

    (
        "%{end}t",
        '[05/Nov/2017:02:01:01 -0500]',
        {
            "end_request_time": datetime(2017,11, 5, 2, 1, 1, tzinfo=w5),
            "end_request_time_fields": {
                "timestamp": datetime(2017,11, 5, 2, 1, 1, tzinfo=w5),
            }
        }
    ),

    (
        "%{begin:}t",
        '[05/Nov/2017:02:01:01 -0500]',
        {
            "begin_request_time": datetime(2017,11, 5, 2, 1, 1, tzinfo=w5),
            "begin_request_time_fields": {
                "timestamp": datetime(2017,11, 5, 2, 1, 1, tzinfo=w5),
            }
        }
    ),

    (
        "%{end:}t",
        '[05/Nov/2017:02:01:01 -0500]',
        {
            "end_request_time": datetime(2017,11, 5, 2, 1, 1, tzinfo=w5),
            "end_request_time_fields": {
                "timestamp": datetime(2017,11, 5, 2, 1, 1, tzinfo=w5),
            }
        }
    ),
])
def test_parse_custom_time(fmt, entry, fields):
    log_entry = LogParser(fmt, encoding='utf-8').parse(entry)
    for k,v in fields.items():
        assert getattr(log_entry, k) == v
