from   datetime    import datetime
from   dateutil.tz import tzutc
import pytest
from   apachelogs  import LogFormat

@pytest.mark.parametrized('fmt,entry,fields', [
    (
        '"%400r" "%r"',
        '"-" "GET /index.html HTTP/1.1"',
        {"request_line": "GET /index.html HTTP/1.1"},
    ),
    (
        '"%r" "%400r"',
        '"GET /index.html HTTP/1.1" "-"',
        {"request_line": "GET /index.html HTTP/1.1"},
    ),
    (
        '"%!400r" "%r"',
        '"-" "GET /index.xml HTTP/1.1"',
        {"request_line": "GET /index.xml HTTP/1.1"},
    ),
    (
        '"%r" "%!400r"',
        '"GET /index.xml HTTP/1.1" "-"',
        {"request_line": "GET /index.xml HTTP/1.1"},
    ),

    (
        '%{%a %b %d}t %r',
        'Sat Nov 25 GET / HTTP/1.1',
        {
            "request_time_abbrev_wday": "Sat",
            "request_time_abbrev_mon": "Nov",
            "request_time_mday": 25,
            "request_line": "GET / HTTP/1.1",
        },
    ),
    (
        '%{%A %B %d}t %r',
        'Saturday November 25 GET / HTTP/1.1',
        {
            "request_time_full_wday": "Saturday",
            "request_time_full_mon": "November",
            "request_time_mday": 25,
            "request_line": "GET / HTTP/1.1",
        },
    ),
    (
        '%{%w (%u) %m/%d}t %r',
        '6 (6) 11/25 GET / HTTP/1.1',
        {
            "request_time_wday": 6,
            "request_time_iso_wday": 6,
            "request_time_mon": 11,
            "request_time_mday": 25,
            "request_line": "GET / HTTP/1.1",
        },
    ),

    (
        '%{%s}t %r',
        '1511642826 GET / HTTP/1.1',
        {
            "request_time_unix": 1511642826,
            "request_datetime": datetime(2017, 11, 25, 20, 47, 6, tzinfo=tzutc()),
            "request_line": "GET / HTTP/1.1",
        },
    ),

])
def test_parse_misc(fmt, entry, fields):
    assert dict(LogFormat(fmt, encoding='utf-8').parse(entry)) == fields
