from   datetime   import datetime, timedelta, timezone
import pytest
from   apachelogs import COMBINED, VHOST_COMBINED, LogParser

@pytest.mark.parametrize('fmt,entry,fields', [
    (
        COMBINED,
        '209.126.136.4 - - [01/Nov/2017:07:28:29 +0000] "GET / HTTP/1.1" 301 521 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"',
        {
            "remote_host": "209.126.136.4",
            "remote_logname": None,
            "remote_user": None,
            "request_time": datetime(2017, 11, 1, 7, 28, 29, tzinfo=timezone.utc),
            "request_line": "GET / HTTP/1.1",
            "final_status": 301,
            "bytes_sent": 521,
            "headers_in": {
                "Referer": None,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
            },
            "directives": {
                 "%h": "209.126.136.4",
                 "%l": None,
                 "%u": None,
                 "%t": datetime(2017, 11, 1, 7, 28, 29, tzinfo=timezone.utc),
                 "%r": "GET / HTTP/1.1",
                 "%>s": 301,
                 "%b": 521,
                 "%{Referer}i": None,
                 "%{User-Agent}i": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
            },
        },
    ),

    (
        '"%400r" "%r"',
        '"-" "GET /index.html HTTP/1.1"',
        {
            "request_line": "GET /index.html HTTP/1.1",
            "directives": {
                "%400r": None,
                "%r": "GET /index.html HTTP/1.1",
            },
        },
    ),

    (
        '"%r" "%400r"',
        '"GET /index.html HTTP/1.1" "-"',
        {
            "request_line": "GET /index.html HTTP/1.1",
            "directives": {
                "%r": "GET /index.html HTTP/1.1",
                "%400r": None,
            },
        },
    ),

    (
        '"%!400r" "%r"',
        '"-" "GET /index.xml HTTP/1.1"',
        {
            "request_line": "GET /index.xml HTTP/1.1",
            "directives": {
                "%!400r": None,
                "%r": "GET /index.xml HTTP/1.1",
            },
        },
    ),

    (
        '"%r" "%!400r"',
        '"GET /index.xml HTTP/1.1" "-"',
        {
            "request_line": "GET /index.xml HTTP/1.1",
            "directives": {
                "%r": "GET /index.xml HTTP/1.1",
                "%!400r": None,
            },
        },
    ),

    (
        '%<s %s %>s',
        '201 202 203',
        {
            "original_status": 201,
            "status": 202,
            "final_status": 203,
            "directives": {
                "%<s": 201,
                "%s": 202,
                "%>s": 203,
            },
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
            "directives": {
                "%<{Referer}i": "http://example.com/original",
                "%{Referer}i": "http://example.com/default",
                "%>{Referer}i": "http://example.com/final",
            },
        },
    ),

    (
        '%T %{ms}T',
        '1 1042',
        {
            "request_duration_seconds": 1,
            "request_duration_milliseconds": 1042,
            "directives": {
                "%T": 1,
                "%{ms}T": 1042,
            },
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
            "directives": {
                "%{%Y}t": 2019,
                "%{%m}t": 5,
                "%{%d}t": 5,
                "%{%H}t": 20,
                "%{%M}t": 49,
                "%{%S}t": 14,
                "%{%z}t": timezone.utc,
                "%{msec_frac}t": 690,
                "%s": 403,
                "%a": "172.21.0.1",
                "%{remote}p": 44782,
                "%A": "172.21.0.2",
                "%p": 80,
                "%m": "GET",
                "%U": "/wsgi/test",
                "%q": "?q=foo",
                "%f": "/usr/local/app/run.wsgi",
                "%P": 16,
                "%{tid}P": 140168282543872,
                "%R": "wsgi-script",
            },
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
            "request_uri": "/wsgi/t\xc3\xa9st",
            "request_query": "",
            "request_file": "/usr/local/app/run.wsgi",
            "pid": 16,
            "tid": 140436276180736,
            "handler": "wsgi-script",
            "directives": {
                "%{%Y}t": 2019,
                "%{%m}t": 5,
                "%{%d}t": 5,
                "%{%H}t": 20,
                "%{%M}t": 56,
                "%{%S}t": 7,
                "%{%z}t": timezone.utc,
                "%{msec_frac}t": 148,
                "%s": 403,
                "%a": "172.22.0.1",
                "%{remote}p": 34488,
                "%A": "172.22.0.2",
                "%p": 80,
                "%m": "GET",
                "%U": "/wsgi/t\xc3\xa9st",
                "%q": "",
                "%f": "/usr/local/app/run.wsgi",
                "%P": 16,
                "%{tid}P": 140436276180736,
                "%R": "wsgi-script",
            }
        },
    ),

    (
        "%200f",
        "-",
        {
            "request_file": None,
            "directives": {
                "%200f": None,
            },
        },
    ),

    (
        "%200f",
        "/var/www/html/index.html",
        {
            "request_file": "/var/www/html/index.html",
            "directives": {
                "%200f": "/var/www/html/index.html",
            },
        },
    ),

    (
        "%200{%Y-%m-%d}t",
        "-",
        {
            "request_time": None,
            "request_time_fields": {
                "year": None,
                "mon": None,
                "mday": None,
            },
            "directives": {
                "%200{%Y}t": None,
                "%200{%m}t": None,
                "%200{%d}t": None,
            },
        },
    ),

    (
        "%200{%Y-%m-%d}t",
        "2019-05-06",
        {
            "request_time": None,
            "request_time_fields": {
                "year": 2019,
                "mon": 5,
                "mday": 6,
            },
            "directives": {
                "%200{%Y}t": 2019,
                "%200{%m}t": 5,
                "%200{%d}t": 6,
            },
        },
    ),

    (
        "%200t",
        "-",
        {
            "request_time": None,
            "request_time_fields": {"timestamp": None},
            "directives": {
                "%200t": None,
            },
        },
    ),

    (
        "%200{}t",
        "-",
        {
            "request_time": None,
            "request_time_fields": {"timestamp": None},
            "directives": {
                "%200{}t": None,
            },
        },
    ),

    (
        VHOST_COMBINED,
        r'www.varonathe.org:80 185.234.218.71 - - [14/Apr/2018:18:39:42 +0000] "GET / HTTP/1.1" 301 539 "-" "}__test|O:21:\"JDatabaseDriverMysqli\":3:{s:4:\"\\0\\0\\0a\";O:17:\"JSimplepieFactory\":0:{}s:21:\"\\0\\0\\0disconnectHandlers\";a:1:{i:0;a:2:{i:0;O:9:\"SimplePie\":5:{s:8:\"sanitize\";O:20:\"JDatabaseDriverMysql\":0:{}s:5:\"cache\";b:1;s:19:\"cache_name_function\";s:6:\"assert\";s:10:\"javascript\";i:9999;s:8:\"feed_url\";s:54:\"eval(base64_decode($_POST[111]));JFactory::get();exit;\";}i:1;s:4:\"init\";}}s:13:\"\\0\\0\\0connection\";i:1;}\xf0\x9d\x8c\x86"',
        {
            "virtual_host": "www.varonathe.org",
            "server_port": 80,
            "remote_host": "185.234.218.71",
            "remote_logname": None,
            "remote_user": None,
            "request_time": datetime(2018, 4, 14, 18, 39, 42, tzinfo=timezone.utc),
            "request_time_fields": {
                "timestamp": datetime(2018, 4, 14, 18, 39, 42, tzinfo=timezone.utc),
            },
            "request_line": "GET / HTTP/1.1",
            "final_status": 301,
            "bytes_out": 539,
            "headers_in": {
                "Referer": None,
                "User-Agent": '}__test|O:21:\"JDatabaseDriverMysqli\":3:{s:4:\"\\0\\0\\0a\";O:17:\"JSimplepieFactory\":0:{}s:21:\"\\0\\0\\0disconnectHandlers\";a:1:{i:0;a:2:{i:0;O:9:\"SimplePie\":5:{s:8:\"sanitize\";O:20:\"JDatabaseDriverMysql\":0:{}s:5:\"cache\";b:1;s:19:\"cache_name_function\";s:6:\"assert\";s:10:\"javascript\";i:9999;s:8:\"feed_url\";s:54:\"eval(base64_decode($_POST[111]));JFactory::get();exit;\";}i:1;s:4:\"init\";}}s:13:\"\\0\\0\\0connection\";i:1;}\xf0\x9d\x8c\x86',
            },
            "directives": {
                "%v": "www.varonathe.org",
                "%p": 80,
                "%h": "185.234.218.71",
                "%l": None,
                "%u": None,
                "%t": datetime(2018, 4, 14, 18, 39, 42, tzinfo=timezone.utc),
                "%r": "GET / HTTP/1.1",
                "%>s": 301,
                "%O": 539,
                "%{Referer}i": None,
                "%{User-Agent}i": '}__test|O:21:\"JDatabaseDriverMysqli\":3:{s:4:\"\\0\\0\\0a\";O:17:\"JSimplepieFactory\":0:{}s:21:\"\\0\\0\\0disconnectHandlers\";a:1:{i:0;a:2:{i:0;O:9:\"SimplePie\":5:{s:8:\"sanitize\";O:20:\"JDatabaseDriverMysql\":0:{}s:5:\"cache\";b:1;s:19:\"cache_name_function\";s:6:\"assert\";s:10:\"javascript\";i:9999;s:8:\"feed_url\";s:54:\"eval(base64_decode($_POST[111]));JFactory::get();exit;\";}i:1;s:4:\"init\";}}s:13:\"\\0\\0\\0connection\";i:1;}\xf0\x9d\x8c\x86',
            },
        },
    ),

    (
        "%<t",
        "[14/Apr/2018:18:39:42 +0000]",
        {
            "original_request_time": datetime(2018, 4, 14, 18, 39, 42, tzinfo=timezone.utc),
            "original_request_time_fields": {
                "timestamp": datetime(2018, 4, 14, 18, 39, 42, tzinfo=timezone.utc),
            },
            "directives": {
                "%<t": datetime(2018, 4, 14, 18, 39, 42, tzinfo=timezone.utc),
            },
        },
    ),

    (
        "%>{%Y-%m-%dT%H:%M:%S}t.%>{usec_frac}t%>{%z}t",
        "2019-05-06T12:09:43.123456-0400",
        {
            "final_request_time": datetime(
                2019, 5, 6, 12, 9, 43, 123456,
                tzinfo=timezone(timedelta(hours=-4)),
            ),
            "final_request_time_fields": {
                "year": 2019,
                "mon": 5,
                "mday": 6,
                "hour": 12,
                "min": 9,
                "sec": 43,
                "usec_frac": 123456,
                "timezone": timezone(timedelta(hours=-4)),
            },
            "directives": {
                "%>{%Y}t": 2019,
                "%>{%m}t": 5,
                "%>{%d}t": 6,
                "%>{%H}t": 12,
                "%>{%M}t": 9,
                "%>{%S}t": 43,
                "%>{usec_frac}t": 123456,
                "%>{%z}t": timezone(timedelta(hours=-4)),
            },
        },
    ),

    (
        "%m %% %U%q %% %H",
        "GET % /index.html?foo % HTTP/1.1",
        {
            "request_method": "GET",
            "request_uri": "/index.html",
            "request_query": "?foo",
            "request_protocol": "HTTP/1.1",
            "directives": {
                "%m": "GET",
                "%U": "/index.html",
                "%q": "?foo",
                "%H": "HTTP/1.1",
            },
        },
    ),

    (
        "%<>s",
        "200",
        {
            "final_status": 200,
            "directives": {
                "%<>s": 200,
            },
        },
    ),

    (
        "%200<T",
        "-",
        {
            "original_request_duration_seconds": None,
            "directives": {
                "%200<T": None,
            },
        },
    ),

    (
        "%>!200T",
        "-",
        {
            "final_request_duration_seconds": None,
            "directives": {
                "%>!200T": None,
            },
        },
    ),

    (
        "%>{s}!200T",
        "-",
        {
            "final_request_duration_seconds": None,
            "directives": {
                "%>{s}!200T": None,
            },
        },
    ),

    (
        "%{s}!200>T",
        "-",
        {
            "final_request_duration_seconds": None,
            "directives": {
                "%{s}!200>T": None,
            },
        },
    ),

    (
        "%<{s}!200>T",
        "-",
        {
            "final_request_duration_seconds": None,
            "directives": {
                "%<{s}!200>T": None,
            },
        },
    ),

    (
        "%><{s}!200>T",
        "-",
        {
            "final_request_duration_seconds": None,
            "directives": {
                "%><{s}!200>T": None,
            },
        },
    ),

    (
        "%<200>T",
        "-",
        {
            "final_request_duration_seconds": None,
            "directives": {
                "%<200>T": None,
            },
        },
    ),

    (
        "%<200<!>T",
        "-",
        {
            "final_request_duration_seconds": None,
            "directives": {
                "%<200<!>T": None,
            },
        },
    ),
])
def test_parse(fmt, entry, fields):
    log_entry = LogParser(fmt).parse(entry)
    assert log_entry.entry == entry.rstrip('\r\n')
    assert log_entry.format == fmt
    for k,v in fields.items():
        assert getattr(log_entry, k) == v
