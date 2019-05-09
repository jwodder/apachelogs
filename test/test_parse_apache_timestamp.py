from   datetime   import datetime, timedelta, timezone
import pytest
from   apachelogs import parse_apache_timestamp

def mktz(hours, mins=0):
    return timezone(timedelta(hours=hours, minutes=mins))

e8  = mktz(8)
e7  = mktz(7)
e5  = mktz(5)
utc = timezone.utc
w4  = mktz(-4)
w5  = mktz(-5)
w7  = mktz(-7)
w8  = mktz(-8)

@pytest.mark.parametrize('ts,dt', [
    ('31/Dec/1969:19:00:00 +0500', datetime(1969,12,31,19, 0, 0, tzinfo=e5)),
    ('[31/Dec/1969:19:00:00 +0500]', datetime(1969,12,31,19, 0, 0, tzinfo=e5)),
    ('[31/Dec/1969:19:00:00 +0500', datetime(1969,12,31,19, 0, 0, tzinfo=e5)),
    ('31/Dec/1969:19:00:00 +0500]', datetime(1969,12,31,19, 0, 0, tzinfo=e5)),
    ('31/Dec/1969:19:00:00 -0500', datetime(1969,12,31,19, 0, 0, tzinfo=w5)),
    (
        '31/Dec/1969:19:00:00 +0130',
        datetime(1969,12,31,19, 0, 0, tzinfo=mktz(1, 30)),
    ),
    (
        '31/Dec/1969:19:00:00 +0030',
        datetime(1969,12,31,19, 0, 0, tzinfo=mktz(0, 30)),
    ),
    (
        '31/Dec/1969:19:00:00 -0030',
        datetime(1969,12,31,19, 0, 0, tzinfo=mktz(-0, -30)),
    ),
    (
        '31/Dec/1969:19:00:00 -0130',
        datetime(1969,12,31,19, 0, 0, tzinfo=mktz(-1, -30)),
    ),
    ('02/Apr/2006:01:59:59 +0800', datetime(2006, 4, 2, 1,59,59, tzinfo=e8)),
    ('02/Apr/2006:01:59:59 -0800', datetime(2006, 4, 2, 1,59,59, tzinfo=w8)),
    ('02/Apr/2006:02:30:00 +0700', datetime(2006, 4, 2, 2,30, 0, tzinfo=e7)),
    ('02/Apr/2006:02:30:00 -0700', datetime(2006, 4, 2, 2,30, 0, tzinfo=w7)),
    ('02/Apr/2006:03:00:01 +0700', datetime(2006, 4, 2, 3, 0, 1, tzinfo=e7)),
    ('02/Apr/2006:03:00:01 -0700', datetime(2006, 4, 2, 3, 0, 1, tzinfo=w7)),
    ('29/Oct/2006:00:59:59 +0700', datetime(2006,10,29, 0,59,59, tzinfo=e7)),
    ('29/Oct/2006:00:59:59 -0700', datetime(2006,10,29, 0,59,59, tzinfo=w7)),
    ('29/Oct/2006:01:30:00 +0700', datetime(2006,10,29, 1,30, 0, tzinfo=e7)),
    ('29/Oct/2006:01:30:00 -0700', datetime(2006,10,29, 1,30, 0, tzinfo=w7)),
    ('29/Oct/2006:01:30:00 +0800', datetime(2006,10,29, 1,30, 0, tzinfo=e8)),
    ('29/Oct/2006:01:30:00 -0800', datetime(2006,10,29, 1,30, 0, tzinfo=w8)),
    ('29/Oct/2006:02:00:01 +0800', datetime(2006,10,29, 2, 0, 1, tzinfo=e8)),
    ('29/Oct/2006:02:00:01 -0800', datetime(2006,10,29, 2, 0, 1, tzinfo=w8)),
    ('13/Feb/2009:18:31:30 +0500', datetime(2009, 2,13,18,31,30, tzinfo=e5)),
    ('13/Feb/2009:18:31:30 -0500', datetime(2009, 2,13,18,31,30, tzinfo=w5)),
    ('01/Jan/2016:00:00:00 -0500', datetime(2016, 1, 1, 0, 0, 0, tzinfo=w5)),
    ('03/Jan/2016:06:00:00 -0500', datetime(2016, 1, 3, 6, 0, 0, tzinfo=w5)),
    ('04/Jan/2016:00:00:00 -0500', datetime(2016, 1, 4, 0, 0, 0, tzinfo=w5)),
    ('05/Jan/2016:01:00:00 -0500', datetime(2016, 1, 5, 1, 0, 0, tzinfo=w5)),
    ('06/Jan/2016:02:00:00 -0500', datetime(2016, 1, 6, 2, 0, 0, tzinfo=w5)),
    ('07/Jan/2016:03:00:00 -0500', datetime(2016, 1, 7, 3, 0, 0, tzinfo=w5)),
    ('08/Jan/2016:04:00:00 -0500', datetime(2016, 1, 8, 4, 0, 0, tzinfo=w5)),
    ('09/Jan/2016:05:00:00 -0500', datetime(2016, 1, 9, 5, 0, 0, tzinfo=w5)),
    ('02/Feb/2016:02:02:02 -0500', datetime(2016, 2, 2, 2, 2, 2, tzinfo=w5)),
    ('29/Feb/2016:03:14:15 -0500', datetime(2016, 2,29, 3,14,15, tzinfo=w5)),
    ('03/Mar/2016:03:03:03 -0500', datetime(2016, 3, 3, 3, 3, 3, tzinfo=w5)),
    ('13/Mar/2016:01:59:59 -0500', datetime(2016, 3,13, 1,59,59, tzinfo=w5)),
    ('13/Mar/2016:03:00:01 -0400', datetime(2016, 3,13, 3, 0, 1, tzinfo=w4)),
    ('13/Mar/2016:03:30:00 -0400', datetime(2016, 3,13, 3,30, 0, tzinfo=w4)),
    ('04/Apr/2016:04:04:04 -0400', datetime(2016, 4, 4, 4, 4, 4, tzinfo=w4)),
    ('05/May/2016:05:05:05 -0400', datetime(2016, 5, 5, 5, 5, 5, tzinfo=w4)),
    ('13/May/2016:13:13:13 -0400', datetime(2016, 5,13,13,13,13, tzinfo=w4)),
    ('06/Jun/2016:06:06:06 -0400', datetime(2016, 6, 6, 6, 6, 6, tzinfo=w4)),
    ('07/Jul/2016:07:07:07 -0400', datetime(2016, 7, 7, 7, 7, 7, tzinfo=w4)),
    ('08/Aug/2016:08:08:08 -0400', datetime(2016, 8, 8, 8, 8, 8, tzinfo=w4)),
    ('09/Sep/2016:09:09:09 -0400', datetime(2016, 9, 9, 9, 9, 9, tzinfo=w4)),
    ('10/Oct/2016:10:10:10 -0400', datetime(2016,10,10,10,10,10, tzinfo=w4)),
    ('06/Nov/2016:00:59:59 -0400', datetime(2016,11, 6, 0,59,59, tzinfo=w4)),
    ('06/Nov/2016:01:30:00 -0400', datetime(2016,11, 6, 1,30, 0, tzinfo=w4)),
    ('06/Nov/2016:01:59:59 -0400', datetime(2016,11, 6, 1,59,59, tzinfo=w4)),
    ('06/Nov/2016:01:00:01 -0500', datetime(2016,11, 6, 1, 0, 1, tzinfo=w5)),
    ('06/Nov/2016:01:30:00 -0500', datetime(2016,11, 6, 1,30, 0, tzinfo=w5)),
    ('06/Nov/2016:02:00:01 -0500', datetime(2016,11, 6, 2, 0, 1, tzinfo=w5)),
    ('07/Nov/2016:15:29:40 -0500', datetime(2016,11, 7,15,29,40, tzinfo=w5)),
    ('11/Nov/2016:11:11:11 -0500', datetime(2016,11,11,11,11,11, tzinfo=w5)),
    ('12/Dec/2016:12:12:12 -0500', datetime(2016,12,12,12,12,12, tzinfo=w5)),
    ('01/Nov/2017:07:28:29 +0000', datetime(2017,11, 1, 7,28,29, tzinfo=utc)),
    ('01/Nov/2017:07:28:29 -0400', datetime(2017,11, 1, 7,28,29, tzinfo=w4)),
    ('05/Nov/2017:01:01:01 -0400', datetime(2017,11, 5, 1, 1, 1, tzinfo=w4)),
    ('05/Nov/2017:01:59:59 -0400', datetime(2017,11, 5, 1,59,59, tzinfo=w4)),
    ('05/Nov/2017:02:01:01 -0400', datetime(2017,11, 5, 2, 1, 1, tzinfo=w4)),
    ('05/Nov/2017:01:01:01 -0500', datetime(2017,11, 5, 1, 1, 1, tzinfo=w5)),
    ('05/Nov/2017:01:59:59 -0500', datetime(2017,11, 5, 1,59,59, tzinfo=w5)),
    ('05/Nov/2017:02:01:01 -0500', datetime(2017,11, 5, 2, 1, 1, tzinfo=w5)),
])
def test_parse_apache_timestamp(ts, dt):
    apts = parse_apache_timestamp(ts)
    assert apts == dt
    assert apts.replace(tzinfo=None) == dt.replace(tzinfo=None)
    assert apts.tzinfo == dt.tzinfo

@pytest.mark.parametrize('ts', [
    '13/Mar/2016:01:59:59 -05:00',
    '13/Mar/2016:01:59:59',
    '13/Mar/2016:01:59:59 -05',
    '13/03/2016:01:59:59 -0500',
    '13/Mar/2016 01:59:59 -0500',
    '13/Mar/2016T01:59:59 -0500',
    '13/Sma/2016:01:59:59 -0500',
])
def test_parse_bad_apache_timestamp(ts):
    with pytest.raises(ValueError) as excinfo:
        parse_apache_timestamp(ts)
    assert str(excinfo.value) == ts
