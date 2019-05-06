from   datetime        import date, datetime, time, timedelta, timezone
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

    (
        {"date": date(2017, 11, 1), "time": time(7, 28, 29)},
        datetime(2017, 11, 1, 7, 28, 29),
    ),

    (
        {"date": date(2017, 11, 1), "time": time(7, 28, 29), "timezone": w4},
        datetime(2017, 11, 1, 7, 28, 29, tzinfo=w4),
    ),

    (
        {"year": 2017, "mon": 11, "mday": 1, "time": time(7, 28, 29)},
        datetime(2017, 11, 1, 7, 28, 29),
    ),

    (
        {"date": date(2017, 11, 1), "hour": 7, "min": 28, "sec": 29},
        datetime(2017, 11, 1, 7, 28, 29),
    ),

    (
        {"year": 2017, "mon": 11, "mday": 1, "hour12": 7, "min": 28, "sec": 29},
        None,
    ),

    (
        {
            "year": 2017,
            "mon": 11,
            "mday": 1,
            "hour12": 7,
            "min": 28,
            "sec": 29,
            "am_pm": "AM",
        },
        datetime(2017, 11, 1, 7, 28, 29),
    ),

    (
        {
            "year": 2017,
            "mon": 11,
            "mday": 1,
            "hour12": 7,
            "min": 28,
            "sec": 29,
            "am_pm": "PM",
        },
        datetime(2017, 11, 1, 19, 28, 29),
    ),

    (
        {
            "year": 2017,
            "mon": 11,
            "mday": 1,
            "hour12": 12,
            "min": 28,
            "sec": 29,
            "am_pm": "AM",
        },
        datetime(2017, 11, 1, 0, 28, 29),
    ),

    (
        {
            "year": 2017,
            "mon": 11,
            "mday": 1,
            "hour12": 12,
            "min": 28,
            "sec": 29,
            "am_pm": "PM",
        },
        datetime(2017, 11, 1, 12, 28, 29),
    ),

    (
        {"milliepoch": 1511642826123},
        datetime(2017, 11, 25, 20, 47, 6, 123000, tzinfo=timezone.utc),
    ),

    (
        {"milliepoch": 1511642826123, "timezone": w4},
        datetime(2017, 11, 25, 16, 47, 6, 123000, tzinfo=w4),
    ),

    (
        {"microepoch": 1511642826123456},
        datetime(2017, 11, 25, 20, 47, 6, 123456, tzinfo=timezone.utc),
    ),

    (
        {"microepoch": 1511642826123456, "timezone": w4},
        datetime(2017, 11, 25, 16, 47, 6, 123456, tzinfo=w4),
    ),

    (
        {"milliepoch": 1511642826123, "epoch": 1511642826},
        datetime(2017, 11, 25, 20, 47, 6, 123000, tzinfo=timezone.utc),
    ),

    (
        {"milliepoch": 1511642826123, "microepoch": 1511642826123456},
        datetime(2017, 11, 25, 20, 47, 6, 123456, tzinfo=timezone.utc),
    ),

    (
        {
            "epoch": 1511642826,
            "milliepoch": 1511642826123,
            "microepoch": 1511642826123456,
        },
        datetime(2017, 11, 25, 20, 47, 6, 123456, tzinfo=timezone.utc),
    ),

    (
        {"year": 2017, "mon": 11, "mday": 1, "hour_min": time(7, 28)},
        None,
    ),

    (
        {
            "year": 2017,
            "mon": 11,
            "mday": 1,
            "hour_min": time(7, 28),
            "sec": 29,
        },
        datetime(2017, 11, 1, 7, 28, 29),
    ),

    (
        {"year": 2017, "yday": 305, "hour": 7, "min": 28, "sec": 29},
        datetime(2017, 11, 1, 7, 28, 29),
    ),

    (
        {
            "century": 20,
            "abbrev_year": 17,
            "mon": 11,
            "mday": 1,
            "hour": 7,
            "min": 28,
            "sec": 29,
        },
        datetime(2017, 11, 1, 7, 28, 29),
    ),

    (
        {
            "year": 2017,
            "full_mon": "November",
            "mday": 1,
            "hour": 7,
            "min": 28,
            "sec": 29,
        },
        datetime(2017, 11, 1, 7, 28, 29),
    ),

    (
        {
            "year": 2017,
            "abbrev_mon": "Nov",
            "mday": 1,
            "hour": 7,
            "min": 28,
            "sec": 29,
        },
        datetime(2017, 11, 1, 7, 28, 29),
    ),

    (
        {
            "year": 2017,
            "mon": 11,
            "mday": 1,
            "hour": 7,
            "min": 28,
            "sec": 29,
            "msec_frac": 123,
        },
        datetime(2017, 11, 1, 7, 28, 29, 123000),
    ),

    (
        {
            "year": 2017,
            "mon": 11,
            "mday": 1,
            "hour": 7,
            "min": 28,
            "sec": 29,
            "usec_frac": 123456,
        },
        datetime(2017, 11, 1, 7, 28, 29, 123456),
    ),

    (
        {"year": 2017, "mday": 1, "hour": 7, "min": 28, "sec": 29},
        None,
    ),

    (
        {"year": 2017, "mon": 11, "hour": 7, "min": 28, "sec": 29},
        None,
    ),

    (
        {"year": 2017, "mon": 11, "mday": 1, "hour": 7, "sec": 29},
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
