.. image:: http://www.repostatus.org/badges/latest/active.svg
    :target: http://www.repostatus.org/#active
    :alt: Project Status: Active — The project has reached a stable, usable
          state and is being actively developed.

.. image:: https://github.com/jwodder/apachelogs/workflows/Test/badge.svg?branch=master
    :target: https://github.com/jwodder/apachelogs/actions?workflow=Test
    :alt: CI Status

.. image:: https://codecov.io/gh/jwodder/apachelogs/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jwodder/apachelogs

.. image:: https://img.shields.io/pypi/pyversions/apachelogs.svg
    :target: https://pypi.org/project/apachelogs/

.. image:: https://img.shields.io/github/license/jwodder/apachelogs.svg
    :target: https://opensource.org/licenses/MIT
    :alt: MIT License

`GitHub <https://github.com/jwodder/apachelogs>`_
| `PyPI <https://pypi.org/project/apachelogs/>`_
| `Documentation <https://apachelogs.readthedocs.io>`_
| `Issues <https://github.com/jwodder/apachelogs/issues>`_
| `Changelog <https://github.com/jwodder/apachelogs/blob/master/CHANGELOG.md>`_

``apachelogs`` parses Apache access log files.  Pass it a `log format string
<http://httpd.apache.org/docs/current/mod/mod_log_config.html>`_ and get back a
parser for logfile entries in that format.  ``apachelogs`` even takes care of
decoding escape sequences and converting things like timestamps, integers, and
bare hyphens to ``datetime`` values, ``int``\s, and ``None``\s.


Installation
============
``apachelogs`` requires Python 3.6 or higher.  Just use `pip
<https://pip.pypa.io>`_ for Python 3 (You have pip, right?) to install
``apachelogs`` and its dependencies::

    python3 -m pip install apachelogs


Examples
========

Parse a single log entry:

>>> from apachelogs import LogParser
>>> parser = LogParser("%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"")
>>> # The above log format is also available as the constant `apachelogs.COMBINED`.
>>> entry = parser.parse('209.126.136.4 - - [01/Nov/2017:07:28:29 +0000] "GET / HTTP/1.1" 301 521 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"\n')
>>> entry.remote_host
'209.126.136.4'
>>> entry.request_time
datetime.datetime(2017, 11, 1, 7, 28, 29, tzinfo=datetime.timezone.utc)
>>> entry.request_line
'GET / HTTP/1.1'
>>> entry.final_status
301
>>> entry.bytes_sent
521
>>> entry.headers_in["Referer"] is None
True
>>> entry.headers_in["User-Agent"]
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
>>> # Log entry components can also be looked up by directive:
>>> entry.directives["%r"]
'GET / HTTP/1.1'
>>> entry.directives["%>s"]
301
>>> entry.directives["%t"]
datetime.datetime(2017, 11, 1, 7, 28, 29, tzinfo=datetime.timezone.utc)

Parse a file full of log entries:

>>> with open('/var/log/apache2/access.log') as fp:  # doctest: +SKIP
...     for entry in parser.parse_lines(fp):
...         print(str(entry.request_time), entry.request_line)
...
2019-01-01 12:34:56-05:00 GET / HTTP/1.1
2019-01-01 12:34:57-05:00 GET /favicon.ico HTTP/1.1
2019-01-01 12:34:57-05:00 GET /styles.css HTTP/1.1
# etc.
