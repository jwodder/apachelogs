from   datetime   import datetime, timezone
import pytest
from   apachelogs import COMBINED, LogParser

ENTRY = '66.240.205.34 - - [18/Nov/2017:12:30:55 +0000] "Gh0st\\xad" 400 0 "-" "-"'

NON_STR_FIELDS = {
    "remote_logname": None,
    "remote_user": None,
    "request_time": datetime(2017, 11, 18, 12, 30, 55, tzinfo=timezone.utc),
    "final_status": 400,
    "bytes_sent": 0,
    "headers_in": {
        "Referer": None,
        "User-Agent": None,
    },
}

def test_bytes_parse():
    log_entry = LogParser(COMBINED, encoding='bytes').parse(ENTRY)
    for k,v in NON_STR_FIELDS.items():
        assert getattr(log_entry, k) == v
    assert log_entry.request_line == log_entry.directives["%r"] == b"Gh0st\xAD"
    assert log_entry.remote_host == log_entry.directives["%h"] \
        == b"66.240.205.34"

def test_parse_latin1():
    log_entry = LogParser(COMBINED).parse(ENTRY)
    for k,v in NON_STR_FIELDS.items():
        assert getattr(log_entry, k) == v
    assert log_entry.request_line == log_entry.directives["%r"] == "Gh0st\xAD"
    assert log_entry.remote_host == log_entry.directives["%h"] \
        == "66.240.205.34"

def test_parse_bad_utf8():
    with pytest.raises(UnicodeDecodeError):
        LogParser(COMBINED, encoding='utf-8').parse(ENTRY)

def test_parse_utf8_surrogateescape():
    log_entry = LogParser(COMBINED, encoding='utf-8', errors='surrogateescape')\
                    .parse(ENTRY)
    for k,v in NON_STR_FIELDS.items():
        assert getattr(log_entry, k) == v
    assert log_entry.request_line == log_entry.directives["%r"] == "Gh0st\uDCAD"
    assert log_entry.remote_host == log_entry.directives["%h"] \
        == "66.240.205.34"

@pytest.mark.parametrize('encoding', [None, 'iso-8859-1', 'utf-8'])
def test_parse_ip_address(encoding):
    assert LogParser('%a', encoding=encoding).parse('127.0.0.1').remote_address\
        == "127.0.0.1"
