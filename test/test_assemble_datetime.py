from   datetime        import datetime, timezone
import pytest
from   apachelogs.util import assemble_datetime

@pytest.mark.parametrize('fields,dt', [
    (
        {
            "remote_host": "209.126.136.4",
            "remote_logname": None,
            "remote_user": None,
            "request_time": "01/Nov/2017:07:28:29 +0000",
            "request_line": "GET / HTTP/1.1",
            "final_status": 301,
            "bytes_sent": 521,
            "header_in": {
                "Referer": None,
                "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
            },
        },
        datetime(2017, 11, 1, 7, 28, 29, tzinfo=timezone.utc),
    ),

    (
        {
            "request_time_unix": 1511642826,
            "request_line": "GET / HTTP/1.1",
        },
        datetime(2017, 11, 25, 20, 47, 6, tzinfo=timezone.utc),
    ),

])
def test_assemble_datetime(fields, dt):
    assemble_datetime(fields)
    if dt is None:
        assert 'request_datetime' not in fields
    else:
        assert 'request_datetime' in fields
        assert fields['request_datetime'] == dt
        assert fields['request_datetime'].replace(tzinfo=None) \
            == dt.replace(tzinfo=None)
        assert fields['request_datetime'].tzinfo == dt.tzinfo
