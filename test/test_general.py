from   datetime   import datetime, timezone
from   pathlib    import Path
import pytest
from   apachelogs import COMBINED, InvalidEntryError, LogEntry, LogParser, \
                            VHOST_COMBINED, parse, parse_lines

def mkentry(entry, format, **attrs):
    logentry = LogEntry(entry, format, [], [])
    logentry.__dict__.update(attrs)
    return logentry

VHOST_COMBINED_LOG_ENTRIES = [
    mkentry(
        'www.varonathe.org:80 203.62.1.80 - - [06/May/2019:06:28:20 +0000] "GET / HTTP/1.1" 301 577 "-" "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0"',
        VHOST_COMBINED,
        virtual_host="www.varonathe.org",
        server_port=80,
        remote_host="203.62.1.80",
        remote_logname=None,
        remote_user=None,
        request_time=datetime(2019, 5, 6, 6, 28, 20, tzinfo=timezone.utc),
        request_time_fields={
            "timestamp": datetime(2019, 5, 6, 6, 28, 20, tzinfo=timezone.utc),
        },
        request_line="GET / HTTP/1.1",
        final_status=301,
        bytes_out=577,
        headers_in={
            "Referer": None,
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0",
        },
        directives={
             "%v": "www.varonathe.org",
             "%p": 80,
             "%h": "203.62.1.80",
             "%l": None,
             "%u": None,
             "%t": datetime(2019, 5, 6, 6, 28, 20, tzinfo=timezone.utc),
             "%r": "GET / HTTP/1.1",
             "%>s": 301,
             "%O": 577,
             "%{Referer}i": None,
             "%{User-Agent}i": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0",
        },
    ),

    mkentry(
        'www.varonathe.org:80 203.62.1.80 - - [06/May/2019:06:28:20 +0000] "GET /robots.txt HTTP/1.1" 301 596 "-" "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0"',
        VHOST_COMBINED,
        virtual_host="www.varonathe.org",
        server_port=80,
        remote_host="203.62.1.80",
        remote_logname=None,
        remote_user=None,
        request_time=datetime(2019, 5, 6, 6, 28, 20, tzinfo=timezone.utc),
        request_time_fields={
            "timestamp": datetime(2019, 5, 6, 6, 28, 20, tzinfo=timezone.utc),
        },
        request_line="GET /robots.txt HTTP/1.1",
        final_status=301,
        bytes_out=596,
        headers_in={
            "Referer": None,
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0",
        },
        directives={
             "%v": "www.varonathe.org",
             "%p": 80,
             "%h": "203.62.1.80",
             "%l": None,
             "%u": None,
             "%t": datetime(2019, 5, 6, 6, 28, 20, tzinfo=timezone.utc),
             "%r": "GET /robots.txt HTTP/1.1",
             "%>s": 301,
             "%O": 596,
             "%{Referer}i": None,
             "%{User-Agent}i": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0",
        },
    ),

    mkentry(
        'www.varonathe.org:80 203.62.1.80 - - [06/May/2019:06:28:21 +0000] "POST /App6079ec68.php HTTP/1.1" 301 606 "-" "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0"',
        VHOST_COMBINED,
        virtual_host="www.varonathe.org",
        server_port=80,
        remote_host="203.62.1.80",
        remote_logname=None,
        remote_user=None,
        request_time=datetime(2019, 5, 6, 6, 28, 21, tzinfo=timezone.utc),
        request_time_fields={
            "timestamp": datetime(2019, 5, 6, 6, 28, 21, tzinfo=timezone.utc),
        },
        request_line="POST /App6079ec68.php HTTP/1.1",
        final_status=301,
        bytes_out=606,
        headers_in={
            "Referer": None,
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0",
        },
        directives={
             "%v": "www.varonathe.org",
             "%p": 80,
             "%h": "203.62.1.80",
             "%l": None,
             "%u": None,
             "%t": datetime(2019, 5, 6, 6, 28, 21, tzinfo=timezone.utc),
             "%r": "POST /App6079ec68.php HTTP/1.1",
             "%>s": 301,
             "%O": 606,
             "%{Referer}i": None,
             "%{User-Agent}i": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0",
        },
    ),

    mkentry(
        'www.varonathe.org:80 203.62.1.80 - - [06/May/2019:06:28:21 +0000] "GET /webdav/ HTTP/1.1" 301 554 "-" "Mozilla/5.0"',
        VHOST_COMBINED,
        virtual_host="www.varonathe.org",
        server_port=80,
        remote_host="203.62.1.80",
        remote_logname=None,
        remote_user=None,
        request_time=datetime(2019, 5, 6, 6, 28, 21, tzinfo=timezone.utc),
        request_time_fields={
            "timestamp": datetime(2019, 5, 6, 6, 28, 21, tzinfo=timezone.utc),
        },
        request_line="GET /webdav/ HTTP/1.1",
        final_status=301,
        bytes_out=554,
        headers_in={
            "Referer": None,
            "User-Agent": "Mozilla/5.0",
        },
        directives={
             "%v": "www.varonathe.org",
             "%p": 80,
             "%h": "203.62.1.80",
             "%l": None,
             "%u": None,
             "%t": datetime(2019, 5, 6, 6, 28, 21, tzinfo=timezone.utc),
             "%r": "GET /webdav/ HTTP/1.1",
             "%>s": 301,
             "%O": 554,
             "%{Referer}i": None,
             "%{User-Agent}i": "Mozilla/5.0",
        },
    ),

    mkentry(
        'www.varonathe.org:80 203.62.1.80 - - [06/May/2019:06:28:21 +0000] "GET /help.php HTTP/1.1" 301 592 "-" "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"',
        VHOST_COMBINED,
        virtual_host="www.varonathe.org",
        server_port=80,
        remote_host="203.62.1.80",
        remote_logname=None,
        remote_user=None,
        request_time=datetime(2019, 5, 6, 6, 28, 21, tzinfo=timezone.utc),
        request_time_fields={
            "timestamp": datetime(2019, 5, 6, 6, 28, 21, tzinfo=timezone.utc),
        },
        request_line="GET /help.php HTTP/1.1",
        final_status=301,
        bytes_out=592,
        headers_in={
            "Referer": None,
            "User-Agent": "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
        },
        directives={
             "%v": "www.varonathe.org",
             "%p": 80,
             "%h": "203.62.1.80",
             "%l": None,
             "%u": None,
             "%t": datetime(2019, 5, 6, 6, 28, 21, tzinfo=timezone.utc),
             "%r": "GET /help.php HTTP/1.1",
             "%>s": 301,
             "%O": 592,
             "%{Referer}i": None,
             "%{User-Agent}i": "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
        },
    ),

    mkentry(
        'www.varonathe.org:80 203.62.1.80 - - [06/May/2019:06:28:22 +0000] "GET /java.php HTTP/1.1" 301 592 "-" "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"',
        VHOST_COMBINED,
        virtual_host="www.varonathe.org",
        server_port=80,
        remote_host="203.62.1.80",
        remote_logname=None,
        remote_user=None,
        request_time=datetime(2019, 5, 6, 6, 28, 22, tzinfo=timezone.utc),
        request_time_fields={
            "timestamp": datetime(2019, 5, 6, 6, 28, 22, tzinfo=timezone.utc),
        },
        request_line="GET /java.php HTTP/1.1",
        final_status=301,
        bytes_out=592,
        headers_in={
            "Referer": None,
            "User-Agent": "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
        },
        directives={
             "%v": "www.varonathe.org",
             "%p": 80,
             "%h": "203.62.1.80",
             "%l": None,
             "%u": None,
             "%t": datetime(2019, 5, 6, 6, 28, 22, tzinfo=timezone.utc),
             "%r": "GET /java.php HTTP/1.1",
             "%>s": 301,
             "%O": 592,
             "%{Referer}i": None,
             "%{User-Agent}i": "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
        },
    ),
]

@pytest.mark.parametrize('end', ['', '\n', '\r', '\r\n'])
def test_parse_general(end):
    ENTRY = '209.126.136.4 - - [01/Nov/2017:07:28:29 +0000] "GET / HTTP/1.1" 301 521 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"'
    parser = LogParser(COMBINED, encoding='utf-8')
    assert parser.format == COMBINED
    parsed = parser.parse(ENTRY + end)
    assert parsed.remote_host == "209.126.136.4"
    assert parsed.remote_logname is None
    assert parsed.remote_user is None
    assert parsed.request_time == datetime(2017, 11, 1, 7, 28, 29, tzinfo=timezone.utc)
    assert parsed.request_line == "GET / HTTP/1.1"
    assert parsed.final_status == 301
    assert parsed.bytes_sent == 521
    assert parsed.headers_in == {
        "Referer": None,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    }
    assert parsed.headers_in["User-Agent"] \
        == parsed.headers_in["USER-AGENT"] \
        == parsed.headers_in["user-agent"] \
        == "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
    assert parsed.entry == ENTRY
    assert parsed.format == COMBINED
    assert parsed.request_time_fields \
        == {"timestamp": datetime(2017, 11, 1, 7, 28, 29, tzinfo=timezone.utc)}
    assert parsed.directives == {
        "%h": "209.126.136.4",
        "%l": None,
        "%u": None,
        "%t": datetime(2017, 11, 1, 7, 28, 29, tzinfo=timezone.utc),
        "%r": "GET / HTTP/1.1",
        "%>s": 301,
        "%b": 521,
        "%{Referer}i": None,
        "%{User-Agent}i": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    }

def test_parse_lines_invalid():
    with (Path(__file__).with_name('data') / 'vhost_combined.log').open() as fp:
        entries = parse_lines(VHOST_COMBINED, fp)
        assert next(entries) == VHOST_COMBINED_LOG_ENTRIES[0]
        assert next(entries) == VHOST_COMBINED_LOG_ENTRIES[1]
        assert next(entries) == VHOST_COMBINED_LOG_ENTRIES[2]
        assert next(entries) == VHOST_COMBINED_LOG_ENTRIES[3]
        with pytest.raises(InvalidEntryError) as excinfo:
            next(entries)
        assert str(excinfo.value) == (
            "Could not match log entry 'Bad line'"
            " against log format {!r}".format(VHOST_COMBINED)
        )
        assert excinfo.value.entry == 'Bad line'
        assert excinfo.value.format == VHOST_COMBINED

def test_parse_lines_ignore_invalid():
    with (Path(__file__).with_name('data') / 'vhost_combined.log').open() as fp:
        entries = parse_lines(VHOST_COMBINED, fp, ignore_invalid=True)
        assert list(entries) == VHOST_COMBINED_LOG_ENTRIES

def test_parse_default_enc(mocker):
    m = mocker.patch('apachelogs.LogParser', spec=LogParser)
    r = parse('%s', '200')
    m.assert_called_once_with('%s', encoding='iso-8859-1', errors=None)
    m.return_value.parse.assert_called_once_with('200')
    assert r is m.return_value.parse.return_value

def test_parse_custom_enc(mocker):
    m = mocker.patch('apachelogs.LogParser', spec=LogParser)
    r = parse('%s', '200', encoding='utf-8', errors='surrogateescape')
    m.assert_called_once_with('%s', encoding='utf-8', errors='surrogateescape')
    m.return_value.parse.assert_called_once_with('200')
    assert r is m.return_value.parse.return_value

def test_parse_lines_default_enc(mocker):
    m = mocker.patch('apachelogs.LogParser', spec=LogParser)
    r = parse_lines('%s', ['200'])
    m.assert_called_once_with('%s', encoding='iso-8859-1', errors=None)
    m.return_value.parse_lines.assert_called_once_with(['200'], False)
    assert r is m.return_value.parse_lines.return_value

def test_parse_lines_custom_enc(mocker):
    m = mocker.patch('apachelogs.LogParser', spec=LogParser)
    r = parse_lines('%s', ['200'], encoding='utf-8', errors='surrogateescape')
    m.assert_called_once_with('%s', encoding='utf-8', errors='surrogateescape')
    m.return_value.parse_lines.assert_called_once_with(['200'], False)
    assert r is m.return_value.parse_lines.return_value

def test_case_insensitive_dicts():
    entry = parse(
        "%{USER}e|%{Content-Type}i|%{flavor}C|%{ssl-secure-reneg}n"
        "|%{Content-Type}o|%{Foo}^ti|%{Baz}^to",
        "www-data|application/x-www-form-urlencoded|chocolate|1|text/html"
        "|Bar|Quux",
    )
    assert entry.env_vars == {"USER": "www-data"}
    assert entry.env_vars["USER"] \
        == entry.env_vars["user"] \
        == entry.env_vars["User"] == "www-data"
    assert entry.headers_in == {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    assert entry.headers_in["Content-Type"] \
        == entry.headers_in["CONTENT-TYPE"] \
        == entry.headers_in["content-type"] \
        == "application/x-www-form-urlencoded"
    assert entry.cookies == {"flavor": "chocolate"}
    assert entry.cookies["flavor"] \
        == entry.cookies["FLAVOR"] \
        == entry.cookies["Flavor"] == "chocolate"
    assert entry.notes == {"ssl-secure-reneg": "1"}
    assert entry.notes["ssl-secure-reneg"] \
        == entry.notes["SSL-SECURE-RENEG"] \
        == entry.notes["SSL-Secure-Reneg"] == "1"
    assert entry.headers_out == {"Content-Type": "text/html"}
    assert entry.headers_out["Content-Type"] \
        == entry.headers_out["CONTENT-TYPE"] \
        == entry.headers_out["content-type"] == "text/html"
    assert entry.trailers_in == {"Foo": "Bar"}
    assert entry.trailers_in["Foo"] \
        == entry.trailers_in["FOO"] \
        == entry.trailers_in["foo"] == "Bar"
    assert entry.trailers_out == {"Baz": "Quux"}
    assert entry.trailers_out["Baz"] \
        == entry.trailers_out["BAZ"] \
        == entry.trailers_out["baz"] == "Quux"
