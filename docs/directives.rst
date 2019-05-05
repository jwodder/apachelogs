.. currentmodule:: apachelogs

.. _directives:

Supported Directives
====================

The following table lists the log format directives supported by this library
along with the names & types of the attributes at which their parsed values are
stored on a `LogEntry`.  The attribute names for the directives are based off
of the names used internally by the Apache source code.

A directive with the ``<`` modifier will be stored at
:samp:`entry.original_{attribute_name}`, and a directive with the ``>``
modifier will be stored at :samp:`entry.final_{attribute_name}`

A type of `str` marked with an asterisk (\*) means that the directive's values
are decoded according to the ``encoding`` option to `LogParser`.

See `the Apache documentation
<http://httpd.apache.org/docs/current/mod/mod_log_config.html>`_ for
information on the meaning of each directive.


.. list-table::
    :header-rows: 1

    * - Directive
      - `LogEntry` Attribute
      - Type
    * - ``%%``
      - N/A
      - N/A
    * - ``%a``
      - ``entry.remote_address``
      - `str`
    * - ``%{c}a``
      - ``entry.remote_client_address``
      - `str`
    * - ``%A``
      - ``entry.local_address``
      - `str`
    * - ``%b``
      - ``entry.bytes_sent``
      - `int` or `None`
    * - ``%B``
      - ``entry.bytes_sent``
      - `int`
    * - :samp:`%\{{name}\}C`
      - :samp:`entry.cookies[{name}]`
      - `str`\*
    * - ``%D``
      - ``entry.request_duration_microseconds``
      - `int`
    * - :samp:`%\{{name}\}e`
      - :samp:`entry.env_vars[{name}]`
      - `str`\*
    * - ``%f``
      - ``entry.request_file``
      - `str`\*
    * - ``%h``
      - ``entry.remote_host``
      - `str`\*
    * - ``%H``
      - ``entry.request_protocol``
      - `str`\* or `None`
    * - :samp:`%\{{name}\}i`
      - :samp:`entry.headers_in[{name}]`
      - `str`\* or `None`
    * - ``%I``
      - ``entry.bytes_in``
      - `int`
    * - ``%k``
      - ``entry.requests_on_connection``
      - `int`
    * - ``%l``
      - ``entry.remote_logname``
      - `str`\* or `None`
    * - ``%m``
      - ``entry.request_method``
      - `str`\* or `None`
    * - :samp:`%\{{name}\}n`
      - :samp:`entry.notes[{name}]`
      - `str`\*
    * - :samp:`%\{{name}\}o`
      - :samp:`entry.headers_out[{name}]`
      - `str`\*
    * - ``%O``
      - ``entry.bytes_out``
      - `int`
    * - ``%p``
      - ``entry.server_port``
      - `int`
    * - ``%{canonical}p``
      - ``entry.server_port``
      - `int`
    * - ``%{local}p``
      - ``entry.local_port``
      - `int`
    * - ``%{remote}p``
      - ``entry.remote_port``
      - `int`
    * - ``%P``
      - ``entry.pid``
      - `int`
    * - ``%{pid}P``
      - ``entry.pid``
      - `int`
    * - ``%{tid}P``
      - ``entry.tid``
      - `int`
    * - ``%q``
      - ``entry.request_query``
      - `str`\*
    * - ``%r``
      - ``entry.request_line``
      - `str`\* or `None`
    * - ``%R``
      - ``entry.handler``
      - `str`\*
    * - ``%s``
      - ``entry.status``
      - `int` or `None`
    * - ``%S``
      - ``entry.bytes_combined``
      - `int`
    * - ``%t``
      - ``entry.request_time_fields["apache_timestamp"]``
      - `str`
    * - ``%{sec}t``
      - ``entry.request_time_fields["epoch"]``
      - `int`
    * - ``%{msec}t``
      - ``entry.request_time_fields["milliepoch"]``
      - `int`
    * - ``%{usec}t``
      - ``entry.request_time_fields["microepoch"]``
      - `int`
    * - ``%{msec_frac}t``
      - ``entry.request_time_fields["msec_frac"]``
      - `int`
    * - ``%{usec_frac}t``
      - ``entry.request_time_fields["usec_frac"]``
      - `int`
    * - :samp:`%\{{strftime_format}\}t`
      - ``entry.request_time_fields`` (See below)
      - (See below)
    * - ``%T``
      - ``entry.request_duration_seconds``
      - `int`
    * - ``%{ms}T``
      - ``entry.request_duration_milliseconds``
      - `int`
    * - ``%{us}T``
      - ``entry.request_duration_microseconds``
      - `int`
    * - ``%{s}T``
      - ``entry.request_duration_seconds``
      - `int`
    * - ``%u``
      - ``entry.remote_user``
      - `str`\* or `None`
    * - ``%U``
      - ``entry.request_uri``
      - `str`\* or `None`
    * - ``%v``
      - ``entry.virtual_host``
      - `str`\*
    * - ``%V``
      - ``entry.server_name``
      - `str`\*
    * - ``%X``
      - ``entry.connection_status``
      - `str`
    * - ``%^FB``
      - ``entry.ttfb``
      - `int` or `None`
    * - :samp:`%\{{name}\}^ti`
      - :samp:`entry.trailers_in[{name}]`
      - `str`\*
    * - :samp:`%\{{name}\}^to`
      - :samp:`entry.trailers_out[{name}]`
      - `str`\*


Supported ``strftime`` Directives
---------------------------------

The following table lists the ``strftime`` directives supported for use in the
parameter of a ``%{*}t`` directive along with the keys & types at which they
are stored in ``entry.request_time_fields``.  See any C documentation for
information on the meaning of each directive.

.. list-table::
    :header-rows: 1

    * - Directive
      - ``request_time_fields`` key
      - Type
    * - ``%%``
      - N/A
      - N/A
    * - ``%a``
      - ``"abbrev_wday"``
      - `str`
    * - ``%A``
      - ``"full_wday"``
      - `str`
    * - ``%b``
      - ``"abbrev_mon"``
      - `str`
    * - ``%B``
      - ``"full_mon"``
      - `str`
    * - ``%C``
      - ``"century"``
      - `int`
    * - ``%d``
      - ``"mday"``
      - `int`
    * - ``%D``
      - ``"date"``
      - `datetime.date`
    * - ``%e``
      - ``"mday"``
      - `int`
    * - ``%F``
      - ``"date"``
      - `datetime.date`
    * - ``%g``
      - ``"abbrev_week_year"``
      - `int`
    * - ``%G``
      - ``"week_year"``
      - `int`
    * - ``%h``
      - ``"abbrev_mon"``
      - `str`
    * - ``%H``
      - ``"hour"``
      - `int`
    * - ``%I``
      - ``"hour12"``
      - `int`
    * - ``%j``
      - ``"yday"``
      - `int`
    * - ``%m``
      - ``"mon"``
      - `int`
    * - ``%M``
      - ``"min"``
      - `int`
    * - ``%n``
      - N/A
      - N/A
    * - ``%p``
      - ``"am_pm"``
      - `str`
    * - ``%R``
      - ``"hour_min"``
      - `datetime.time`
    * - ``%s``
      - ``"epoch"``
      - `int`
    * - ``%S``
      - ``"sec"``
      - `int`
    * - ``%t``
      - N/A
      - N/A
    * - ``%T``
      - ``"time"``
      - `datetime.time`
    * - ``%u``
      - ``"iso_wday"``
      - `int`
    * - ``%U``
      - ``"sunday_weeknum"``
      - `int`
    * - ``%V``
      - ``"iso_weeknum"``
      - `int`
    * - ``%w``
      - ``"wday"``
      - `int`
    * - ``%W``
      - ``"monday_weeknum"``
      - `int`
    * - ``%y``
      - ``"abbrev_year"``
      - `int`
    * - ``%Y``
      - ``"year"``
      - `int`
    * - ``%z``
      - ``"timezone"``
      - `datetime.timezone` or `None`
    * - ``%Z``
      - ``"tzname"``
      - `str`