from   datetime        import datetime, timezone
import pytest
from   apachelogs.util import assemble_datetime

@pytest.mark.parametrize('fields,dt', [
    (
        {"apache_timestamp": "01/Nov/2017:07:28:29 +0000"},
        datetime(2017, 11, 1, 7, 28, 29, tzinfo=timezone.utc),
    ),

    (
        {"unix": 1511642826},
        datetime(2017, 11, 25, 20, 47, 6, tzinfo=timezone.utc),
    ),

])
def test_assemble_datetime(fields, dt):
    res = assemble_datetime(fields)
    if dt is None:
        assert res is None
    else:
        assert res == dt
        assert res.replace(tzinfo=None) == dt.replace(tzinfo=None)
        assert res.tzinfo == dt.tzinfo
