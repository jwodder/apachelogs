from   datetime   import datetime, timezone
import pytest
from   apachelogs import COMBINED, LogParser

ENTRY = '209.126.136.4 - - [01/Nov/2017:07:28:29 +0000] "GET / HTTP/1.1" 301 521 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"'

@pytest.mark.xfail(reason='TODO')
def test_parse_general():
    parsed = LogParser(COMBINED, encoding='utf-8').parse(ENTRY)
    assert dict(parsed) == {
        "remote_host": "209.126.136.4",
        "remote_logname": None,
        "remote_user": None,
        "request_time": datetime(2017, 11, 1, 7, 28, 29, tzinfo=timezone.utc),
        "request_line": "GET / HTTP/1.1",
        "final_status": 301,
        "bytes_sent": 521,
        "header_in": {
            "Referer": None,
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
        },
    }
    assert parsed.entry == ENTRY
    assert parsed["header_in"]["User-agent"] == \
        parsed["header_in"]["USER-AGENT"] == \
        parsed["header_in"]["user-agent"] == \
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
    assert parsed.time_fields == \
        {"apache_timestamp": "01/Nov/2017:07:28:29 +0000"}
