from   datetime   import datetime, timezone
import pytest
from   apachelogs import LogParser

@pytest.mark.parametrize('fmt,entry,fields', [
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
        '%<s %s %>s',
        '201 202 203',
        {
            "original_status": 201,
            "status": 202,
            "final_status": 203,
        },
    ),
    (
        '%<{Referer}i %{Referer}i %>{Referer}i',
        'http://example.com/original http://example.com/default http://example.com/final',
        {
            "original_headers_in": {
                "Referer": "http://example.com/original",
            },
            "headers_in": {
                "Referer": "http://example.com/default",
            },
            "final_headers_in": {
                "Referer": "http://example.com/final",
            },
        },
    ),
    (
        '%T %{ms}T',
        '1 1042',
        {
            "request_duration_seconds": 1,
            "request_duration_milliseconds": 1042,
        }
    ),
    (
        "%{%Y-%m-%d %H:%M:%S %z}t [%{msec_frac}t] %s %a:%{remote}p <-> %A:%p \"%m\" \"%U%q\" \"%f\" %P:%{tid}P \"%R\"",
        '2019-05-05 20:49:14 +0000 [690] 403 172.21.0.1:44782 <-> 172.21.0.2:80 "GET" "/wsgi/test?q=foo" "/usr/local/app/run.wsgi" 16:140168282543872 "wsgi-script"',
        {
            "request_time": datetime(2019, 5, 5, 20, 49, 14, 690000,
                                     tzinfo=timezone.utc),
            "request_time_fields": {
                "year": 2019,
                "mon": 5,
                "mday": 5,
                "hour": 20,
                "min": 49,
                "sec": 14,
                "timezone": timezone.utc,
                "msec_frac": 690,
            },
            "status": 403,
            "remote_address": "172.21.0.1",
            "remote_port": 44782,
            "local_address": "172.21.0.2",
            "server_port": 80,
            "request_method": "GET",
            "request_uri": "/wsgi/test",
            "request_query": "?q=foo",
            "request_file": "/usr/local/app/run.wsgi",
            "pid": 16,
            "tid": 140168282543872,
            "handler": "wsgi-script",
        },
    ),
    (
        "%{%Y-%m-%d %H:%M:%S %z}t [%{msec_frac}t] %s %a:%{remote}p <-> %A:%p \"%m\" \"%U%q\" \"%f\" %P:%{tid}P \"%R\"",
        r'2019-05-05 20:56:07 +0000 [148] 403 172.22.0.1:34488 <-> 172.22.0.2:80 "GET" "/wsgi/t\xc3\xa9st" "/usr/local/app/run.wsgi" 16:140436276180736 "wsgi-script"',
        {
            "request_time": datetime(2019, 5, 5, 20, 56, 7, 148000,
                                     tzinfo=timezone.utc),
            "request_time_fields": {
                "year": 2019,
                "mon": 5,
                "mday": 5,
                "hour": 20,
                "min": 56,
                "sec": 7,
                "timezone": timezone.utc,
                "msec_frac": 148,
            },
            "status": 403,
            "remote_address": "172.22.0.1",
            "remote_port": 34488,
            "local_address": "172.22.0.2",
            "server_port": 80,
            "request_method": "GET",
            "request_uri": "/wsgi/tést",
            "request_query": "",
            "request_file": "/usr/local/app/run.wsgi",
            "pid": 16,
            "tid": 140436276180736,
            "handler": "wsgi-script",
        },
    ),
])
def test_parse_misc(fmt, entry, fields):
    log_entry = LogParser(fmt, encoding='utf-8').parse(entry)
    for k,v in fields.items():
        assert getattr(log_entry, k) == v
