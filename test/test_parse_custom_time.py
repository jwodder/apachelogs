from   datetime   import datetime, timedelta, timezone
import pytest
from   apachelogs import LogParser

w5 = timezone(timedelta(hours=-5))

@pytest.mark.parametrize('fmt,entry,fields,time_fields', [
    (
        '%{%a %b %d}t %r',
        'Sat Nov 25 GET / HTTP/1.1',
        {
            "request_line": "GET / HTTP/1.1",
            "request_time": None,
        },
        {
            "abbrev_wday": "Sat",
            "abbrev_mon": "Nov",
            "mday": 25,
        },
    ),

    (
        '%{%A %B %d}t %r',
        'Saturday November 25 GET / HTTP/1.1',
        {
            "request_line": "GET / HTTP/1.1",
            "request_time": None,
        },
        {
            "full_wday": "Saturday",
            "full_mon": "November",
            "mday": 25,
        }
    ),

    (
        '%{%w (%u) %m/%d}t %r',
        '6 (6) 11/25 GET / HTTP/1.1',
        {
            "request_line": "GET / HTTP/1.1",
            "request_time": None,
        },
        {
            "wday": 6,
            "iso_wday": 6,
            "mon": 11,
            "mday": 25,
        }
    ),

    (
        '%{%s}t %r',
        '1511642826 GET / HTTP/1.1',
        {
            "request_line": "GET / HTTP/1.1",
            "request_time": datetime(2017, 11, 25, 20, 47, 6, tzinfo=timezone.utc),
        },
        {"epoch": 1511642826},
    ),

    (
        '%{%s@%z}t %r',
        '1511642826@-0500 GET / HTTP/1.1',
        {
            "request_line": "GET / HTTP/1.1",
            "request_time": datetime(2017, 11, 25, 15, 47, 6, tzinfo=w5),
        },
        {"epoch": 1511642826, "timezone": w5},
    ),

    (
        '%{%Y-%m-%d %H:%M:%S}t %r',
        '2017-11-25 20:47:06 GET / HTTP/1.1',
        {
            "request_line": "GET / HTTP/1.1",
            "request_time": datetime(2017, 11, 25, 20, 47, 6),
        },
        {
            "year": 2017,
            "mon": 11,
            "mday": 25,
            "hour": 20,
            "min": 47,
            "sec": 6,
        },
    ),

    (
        '%{%Y-%m-%d %H:%M:%S %z}t %r',
        '2017-11-25 20:47:06 -0500 GET / HTTP/1.1',
        {
            "request_line": "GET / HTTP/1.1",
            "request_time": datetime(2017, 11, 25, 20, 47, 6, tzinfo=w5),
        },
        {
            "year": 2017,
            "mon": 11,
            "mday": 25,
            "hour": 20,
            "min": 47,
            "sec": 6,
            "timezone": w5,
        },
    ),

    (
        '%{%s}t@%{%z}t %r',
        '1511642826@-0500 GET / HTTP/1.1',
        {
            "request_line": "GET / HTTP/1.1",
            "request_time": datetime(2017, 11, 25, 15, 47, 6, tzinfo=w5),
        },
        {"epoch": 1511642826, "timezone": w5},
    ),

    (
        '%{%Y-%m-%d}t %{%H:%M:%S}t %r',
        '2017-11-25 20:47:06 GET / HTTP/1.1',
        {
            "request_line": "GET / HTTP/1.1",
            "request_time": datetime(2017, 11, 25, 20, 47, 6),
        },
        {
            "year": 2017,
            "mon": 11,
            "mday": 25,
            "hour": 20,
            "min": 47,
            "sec": 6,
        },
    ),

    (
        '%{%Y-%m-%d}t %{%H:%M:%S}t %{%z}t %r',
        '2017-11-25 20:47:06 -0500 GET / HTTP/1.1',
        {
            "request_line": "GET / HTTP/1.1",
            "request_time": datetime(2017, 11, 25, 20, 47, 6, tzinfo=w5),
        },
        {
            "year": 2017,
            "mon": 11,
            "mday": 25,
            "hour": 20,
            "min": 47,
            "sec": 6,
            "timezone": w5,
        },
    ),
])
def test_parse_custom_time(fmt, entry, fields, time_fields):
    res = LogParser(fmt, encoding='utf-8').parse(entry)
    assert dict(res) == fields
    assert res.time_fields == time_fields
