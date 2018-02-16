import pytest
from   apachelogs import LogFormat

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
])
def test_parse_misc(fmt, entry, fields):
    assert dict(LogFormat(fmt, encoding='utf-8').parse(entry)) == fields
