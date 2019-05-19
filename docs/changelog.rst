.. currentmodule:: apachelogs

Changelog
=========

v0.4.0 (2019-05-19)
-------------------
- Support the ``%{c}h`` log directive
- ``%f`` and ``%R`` can now be `None`
- **Bugfix**: ``%u`` can now match the string ``""`` (two double quotes)
- Support ``mod_ssl``'s ``%{*}c`` and ``%{*}x`` directives
- Support the ``%{hextid}P`` directive (as a hexadecimal integer)
- Support the ``%L`` and ``%{c}L`` directives
- Parameters to ``%{*}p``, ``%{*}P``, and ``%{*}T`` are now treated
  case-insensitively in order to mirror Apache's behavior
- Refined some directives to better match only the values emitted by Apache:
    - ``%l`` and ``%m`` no longer accept whitespace
    - ``%s`` and ``%{tid}P`` now only match unsigned integers
    - ``%{*}C`` no longer accepts semicolons or leading or trailing spaces
    - ``%q`` no longer accepts whitespace or pound/hash signs

v0.3.0 (2019-05-12)
-------------------
- Gave `LogEntry` a `~LogEntry.directives` attribute for looking up directive
  values by the corresponding log format directives

v0.2.0 (2019-05-09)
-------------------
- Changed the capitalization of "User-agent" in the log format string constants
  to "User-Agent"
- The ``cookies``, ``env_vars``, ``headers_in``, ``headers_out``, ``notes``,
  ``trailers_in``, and ``trailers_out`` attributes of `LogEntry` are now all
  case-insensitive `dict`\s.

v0.1.0 (2019-05-06)
-------------------
Initial release
