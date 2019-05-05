from   datetime        import datetime, timedelta, timezone
import pytest
from   apachelogs.util import assemble_datetime

w4 = timezone(timedelta(hours=-4))

@pytest.mark.parametrize('fields,dt', [
    (
        {"timestamp": datetime(2017, 11, 1, 7, 28, 29, tzinfo=timezone.utc)},
        datetime(2017, 11, 1, 7, 28, 29, tzinfo=timezone.utc),
    ),

    (
        {
            "timestamp": datetime(2017, 11, 1, 7, 28, 29, tzinfo=timezone.utc),
            "timezone": w4,
        },
        datetime(2017, 11, 1, 7, 28, 29, tzinfo=timezone.utc),
    ),

    (
        {"epoch": 1511642826},
        datetime(2017, 11, 25, 20, 47, 6, tzinfo=timezone.utc),
    ),

    (
        {"epoch": 1511642826, "timezone": w4},
        datetime(2017, 11, 25, 16, 47, 6, tzinfo=w4),
    ),

    (
        {
            "year": 2017,
            "mon": 11,
            "mday": 1,
            "hour": 7,
            "min": 28,
            "sec": 29,
            "timezone": w4,
        },
        datetime(2017, 11, 1, 7, 28, 29, tzinfo=w4),
    ),

    (
        {"year": 2017, "mon": 11, "mday": 1, "hour": 7, "min": 28, "sec": 29},
        datetime(2017, 11, 1, 7, 28, 29),
    ),

    (
        {"year": 2017, "mon": 11, "mday": 1, "hour": 7, "min": 28},
        None,
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
