.. image:: http://www.repostatus.org/badges/latest/wip.svg
    :target: http://www.repostatus.org/#wip
    :alt: Project Status: WIP — Initial development is in progress, but there
          has not yet been a stable, usable release suitable for the public.

.. image:: https://travis-ci.com/jwodder/apachelogs.svg?branch=master
    :target: https://travis-ci.com/jwodder/apachelogs

.. image:: https://codecov.io/gh/jwodder/apachelogs/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jwodder/apachelogs

.. image:: https://img.shields.io/github/license/jwodder/apachelogs.svg
    :target: https://opensource.org/licenses/MIT
    :alt: MIT License

.. image:: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg
    :target: https://saythanks.io/to/jwodder

`GitHub <https://github.com/jwodder/apachelogs>`_
| `Issues <https://github.com/jwodder/apachelogs/issues>`_

``apachelogs`` parses Apache access log files.  Pass it a logfile format
string, and you'll get back a parser for logfile entries in that format.


Installation
============
``apachelogs`` requires Python 3.5 or higher.  Just use `pip
<https://pip.pypa.io>`_ for Python 3 (You have pip, right?) to install
``apachelogs`` and its dependencies::

    python3 -m pip install git+https://github.com/jwodder/apachelogs.git


Example
=======

::

    >>> from apachelogs import LogParser
    >>> parser = LogParser("%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"")
    >>> # The above log format is also available as the constant `apachelogs.COMBINED`
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
    >>> entry.headers_in["User-agent"]
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
