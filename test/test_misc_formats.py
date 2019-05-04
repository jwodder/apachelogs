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
            "original_header_in": {
                "Referer": "http://example.com/original",
            },
            "header_in": {
                "Referer": "http://example.com/default",
            },
            "final_header_in": {
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
])
def test_parse_misc(fmt, entry, fields):
    assert dict(LogParser(fmt, encoding='utf-8').parse(entry)) == fields
