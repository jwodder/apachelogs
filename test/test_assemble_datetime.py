from   datetime            import date, datetime, time, timedelta, timezone
import pytest
from   apachelogs.timeutil import assemble_datetime

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
            "century": 20,
            "mon": 11,
            "mday": 1,
            "hour": 7,
            "min": 28,
            "sec": 29,
        },
        None,
    ),

    (
        {
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
            "abbrev_year": 0,
            "mon": 11,
            "mday": 1,
            "hour": 7,
            "min": 28,
            "sec": 29,
        },
        datetime(2000, 11, 1, 7, 28, 29),
    ),

    (
        {
            "abbrev_year": 68,
            "mon": 11,
            "mday": 1,
            "hour": 7,
            "min": 28,
            "sec": 29,
        },
        datetime(2068, 11, 1, 7, 28, 29),
    ),

    (
        {
            "abbrev_year": 69,
            "mon": 11,
            "mday": 1,
            "hour": 7,
            "min": 28,
            "sec": 29,
        },
        datetime(1969, 11, 1, 7, 28, 29),
    ),

    (
        {
            "abbrev_year": 99,
            "mon": 11,
            "mday": 1,
            "hour": 7,
            "min": 28,
            "sec": 29,
        },
        datetime(1999, 11, 1, 7, 28, 29),
    ),

    (
        {
            "century": 19,
            "abbrev_year": 0,
            "mon": 11,
            "mday": 1,
            "hour": 7,
            "min": 28,
            "sec": 29,
        },
        datetime(1900, 11, 1, 7, 28, 29),
    ),

    (
        {
            "century": 19,
            "abbrev_year": 68,
            "mon": 11,
            "mday": 1,
            "hour": 7,
            "min": 28,
            "sec": 29,
        },
        datetime(1968, 11, 1, 7, 28, 29),
    ),

    (
        {
            "century": 20,
            "abbrev_year": 69,
            "mon": 11,
            "mday": 1,
            "hour": 7,
            "min": 28,
            "sec": 29,
        },
        datetime(2069, 11, 1, 7, 28, 29),
    ),

    (
        {
            "century": 20,
            "abbrev_year": 99,
            "mon": 11,
            "mday": 1,
            "hour": 7,
            "min": 28,
            "sec": 29,
        },
        datetime(2099, 11, 1, 7, 28, 29),
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

    (
        {
            "iso_year": 2019,
            "iso_weeknum": 20,
            "iso_wday": 7,
            "time": time(12, 34, 56),
        },
        datetime(2019, 5, 19, 12, 34, 56),
    ),

    (
        {
            "iso_year": 2019,
            "iso_weeknum": 20,
            "wday": 0,
            "time": time(12, 34, 56),
        },
        datetime(2019, 5, 19, 12, 34, 56),
    ),

    (
        {
            "iso_year": 2019,
            "iso_weeknum": 20,
            "abbrev_wday": "Sun",
            "time": time(12, 34, 56),
        },
        datetime(2019, 5, 19, 12, 34, 56),
    ),

    (
        {
            "iso_year": 2019,
            "iso_weeknum": 20,
            "full_wday": "Sunday",
            "time": time(12, 34, 56),
        },
        datetime(2019, 5, 19, 12, 34, 56),
    ),

    (
        {
            "iso_year": 2019,
            "iso_weeknum": 52,
            "iso_wday": 7,
            "time": time(12, 34, 56),
        },
        datetime(2019, 12, 29, 12, 34, 56),
    ),

    (
        {
            "iso_year": 2020,
            "iso_weeknum": 1,
            "iso_wday": 1,
            "time": time(12, 34, 56),
        },
        datetime(2019, 12, 30, 12, 34, 56),
    ),

    (
        {
            "abbrev_iso_year": 19,
            "iso_weeknum": 20,
            "iso_wday": 7,
            "time": time(12, 34, 56),
        },
        datetime(2019, 5, 19, 12, 34, 56),
    ),

    (
        {
            "abbrev_iso_year": 0,
            "iso_weeknum": 20,
            "iso_wday": 5,
            "time": time(12, 34, 56),
        },
        datetime(2000, 5, 19, 12, 34, 56),
    ),

    (
        {
            "abbrev_iso_year": 68,
            "iso_weeknum": 20,
            "iso_wday": 6,
            "time": time(12, 34, 56),
        },
        datetime(2068, 5, 19, 12, 34, 56),
    ),

    (
        {
            "abbrev_iso_year": 69,
            "iso_weeknum": 21,
            "iso_wday": 1,
            "time": time(12, 34, 56),
        },
        datetime(1969, 5, 19, 12, 34, 56),
    ),

    (
        {
            "abbrev_iso_year": 99,
            "iso_weeknum": 20,
            "iso_wday": 3,
            "time": time(12, 34, 56),
        },
        datetime(1999, 5, 19, 12, 34, 56),
    ),

    (
        {
            "year": 2019,
            "sunday_weeknum": 20,
            "wday": 0,
            "time": time(12, 34, 56),
        },
        datetime(2019, 5, 19, 12, 34, 56),
    ),

    (
        {
            "year": 2019,
            "sunday_weeknum": 20,
            "iso_wday": 7,
            "time": time(12, 34, 56),
        },
        datetime(2019, 5, 19, 12, 34, 56),
    ),

    (
        {
            "year": 2019,
            "sunday_weeknum": 20,
            "full_wday": "Sunday",
            "time": time(12, 34, 56),
        },
        datetime(2019, 5, 19, 12, 34, 56),
    ),

    (
        {
            "year": 2019,
            "sunday_weeknum": 20,
            "abbrev_wday": "Sun",
            "time": time(12, 34, 56),
        },
        datetime(2019, 5, 19, 12, 34, 56),
    ),

    (
        {
            "year": 2019,
            "monday_weeknum": 19,
            "wday": 0,
            "time": time(12, 34, 56),
        },
        datetime(2019, 5, 19, 12, 34, 56),
    ),

    (
        {
            "year": 2019,
            "monday_weeknum": 19,
            "iso_wday": 7,
            "time": time(12, 34, 56),
        },
        datetime(2019, 5, 19, 12, 34, 56),
    ),

    (
        {
            "year": 2019,
            "monday_weeknum": 19,
            "full_wday": "Sunday",
            "time": time(12, 34, 56),
        },
        datetime(2019, 5, 19, 12, 34, 56),
    ),

    (
        {
            "year": 2019,
            "monday_weeknum": 19,
            "abbrev_wday": "Sun",
            "time": time(12, 34, 56),
        },
        datetime(2019, 5, 19, 12, 34, 56),
    ),

    (
        {
            "abbrev_year": 0,
            "sunday_weeknum": 20,
            "wday": 0,
            "time": time(12, 34, 56),
        },
        datetime(2000, 5, 14, 12, 34, 56),
    ),

    (
        {
            "abbrev_year": 68,
            "sunday_weeknum": 20,
            "wday": 0,
            "time": time(12, 34, 56),
        },
        datetime(2068, 5, 13, 12, 34, 56),
    ),

    (
        {
            "abbrev_year": 69,
            "sunday_weeknum": 20,
            "wday": 0,
            "time": time(12, 34, 56),
        },
        datetime(1969, 5, 18, 12, 34, 56),
    ),

    (
        {
            "abbrev_year": 99,
            "sunday_weeknum": 20,
            "wday": 0,
            "time": time(12, 34, 56),
        },
        datetime(1999, 5, 16, 12, 34, 56),
    ),

    (
        {
            "abbrev_year": 0,
            "monday_weeknum": 20,
            "wday": 0,
            "time": time(12, 34, 56),
        },
        datetime(2000, 5, 21, 12, 34, 56),
    ),

    (
        {
            "abbrev_year": 68,
            "monday_weeknum": 20,
            "wday": 0,
            "time": time(12, 34, 56),
        },
        datetime(2068, 5, 20, 12, 34, 56),
    ),

    (
        {
            "abbrev_year": 69,
            "monday_weeknum": 20,
            "wday": 0,
            "time": time(12, 34, 56),
        },
        datetime(1969, 5, 25, 12, 34, 56),
    ),

    (
        {
            "abbrev_year": 99,
            "monday_weeknum": 20,
            "wday": 0,
            "time": time(12, 34, 56),
        },
        datetime(1999, 5, 23, 12, 34, 56),
    ),

    (
        {
            "century": 19,
            "abbrev_year": 0,
            "sunday_weeknum": 20,
            "wday": 0,
            "time": time(12, 34, 56),
        },
        datetime(1900, 5, 20, 12, 34, 56),
    ),

    (
        {
            "century": 19,
            "abbrev_year": 68,
            "sunday_weeknum": 20,
            "wday": 0,
            "time": time(12, 34, 56),
        },
        datetime(1968, 5, 19, 12, 34, 56),
    ),

    (
        {
            "century": 20,
            "abbrev_year": 69,
            "sunday_weeknum": 20,
            "wday": 0,
            "time": time(12, 34, 56),
        },
        datetime(2069, 5, 19, 12, 34, 56),
    ),

    (
        {
            "century": 20,
            "abbrev_year": 99,
            "sunday_weeknum": 20,
            "wday": 0,
            "time": time(12, 34, 56),
        },
        datetime(2099, 5, 17, 12, 34, 56),
    ),

    (
        {
            "century": 19,
            "abbrev_year": 0,
            "monday_weeknum": 20,
            "wday": 0,
            "time": time(12, 34, 56),
        },
        datetime(1900, 5, 20, 12, 34, 56),
    ),

    (
        {
            "century": 19,
            "abbrev_year": 68,
            "monday_weeknum": 20,
            "wday": 0,
            "time": time(12, 34, 56),
        },
        datetime(1968, 5, 19, 12, 34, 56),
    ),

    (
        {
            "century": 20,
            "abbrev_year": 69,
            "monday_weeknum": 20,
            "wday": 0,
            "time": time(12, 34, 56),
        },
        datetime(2069, 5, 26, 12, 34, 56),
    ),

    (
        {
            "century": 20,
            "abbrev_year": 99,
            "monday_weeknum": 20,
            "wday": 0,
            "time": time(12, 34, 56),
        },
        datetime(2099, 5, 24, 12, 34, 56),
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
