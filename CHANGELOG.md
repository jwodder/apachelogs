v0.7.0 (in development)
-----------------------
- Support Python 3.9
- Drop support for Python 3.5

v0.6.0 (2020-10-13)
-------------------
- Support Python 3.8
- `%s` now matches any sequence of exactly three digits.  Previously, it
  matched either '0' or any sequence of digits not beginning with '0'.  Thanks
  to [@chosak](https://github.com/chosak) for the patch.

v0.5.0 (2019-05-21)
-------------------
- Improved the routine for assembling `request_time` from
  `request_time_fields`:
    - If the month is only available as a full or abbreviated name and the name
      is not in English, try looking it up in the current locale
    - If the year is only available in abbreviated form (the `%y` directive)
      without a century (`%C`), treat years less than 69 as part of the
      twenty-first century and other years as part of the twentieth
    - When necessary, use the values of the `%G`, `%g`, `%u`, `%V`, `%U`, `%W`,
      and `%w` time directives to derive the date
    - If `%Z` equals `"GMT"`, `"UTC"`, or one of the names in `time.tzname`,
      produce an aware `datetime`
- `%{%n}t` and `%{%t}t` now match any amount of any whitespace, in order to
  match `strptime(3)`'s behavior
- **Breaking**: Renamed the `request_time_fields` keys for `%{%G}t` and
  `%{%g}t` from `"week_year"` and `"abbrev_week_year"` to `"iso_year"` and
  `"abbrev_iso_year"`, respectively
- `%{%p}t` can now match the empty string (its value in certain locales)
- `%{%Z}t` can now match the empty string

v0.4.0 (2019-05-19)
-------------------
- Support the `%{c}h` log directive
- `%f` and `%R` can now be `None`
- **Bugfix**: `%u` can now match the string `""` (two double quotes)
- Support `mod_ssl`'s `%{*}c` and `%{*}x` directives
- Support the `%{hextid}P` directive (as a hexadecimal integer)
- Support the `%L` and `%{c}L` directives
- Parameters to `%{*}p`, `%{*}P`, and `%{*}T` are now treated
  case-insensitively in order to mirror Apache's behavior
- Refined some directives to better match only the values emitted by Apache:
    - `%l` and `%m` no longer accept whitespace
    - `%s` and `%{tid}P` now only match unsigned integers
    - `%{*}C` no longer accepts semicolons or leading or trailing spaces
    - `%q` no longer accepts whitespace or pound/hash signs

v0.3.0 (2019-05-12)
-------------------
- Gave `LogEntry` a `directives` attribute for looking up directive values by
  the corresponding log format directives

v0.2.0 (2019-05-09)
-------------------
- Changed the capitalization of "User-agent" in the log format string constants
  to "User-Agent"
- The `cookies`, `env_vars`, `headers_in`, `headers_out`, `notes`,
  `trailers_in`, and `trailers_out` attributes of `LogEntry` are now all
  case-insensitive `dict`s.

v0.1.0 (2019-05-06)
-------------------
Initial release
