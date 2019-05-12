.. currentmodule:: apachelogs

Changelog
=========

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
