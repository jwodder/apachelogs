- `apachelogs.format` — contains string (and compiled `LogEntryParser`?)
  constants for common, combined, etc. formats
- `compile(format: str, humanize=False) -> LogEntryParser`
- `LogEntryParser` (`ApacheLogParser`? `Parser`?)
    - `match(entry: str) -> dict`
        - Rename to `parse`?
- `fmtstr2regex(fmt: str)` ?
- helper function for converting a match object to a result dict?
- `match(fmt, entry, humanize=False) -> dict`
- `match_lines(fmt, entries: Iterator[str], humanize=False) -> Iterator[dict]`
- `apachelogs2json [--format <format>] [<file> ...]`
    - The special names "combined" and "common" (et alii?) are accepted as
      formats.
        - Accept these in the library interface as well?
    - Default format: combined?  Guess at combined or common?
- `ValueError` subclass for invalid log format directives
- `ValueError` subclass for invalid/non-matching log entries

- If the same format directive (or two different directives with the same name,
  e.g., `%B` and `%b`?) appears more than once in a format, it is assumed that
  the field's value remains constant throughout each individual record, and
  thus all but one of the occurrences (the first? the last?) are discarded

- Give the `match` functions a way to return a dict that uses the format
  directives instead of custom names as keys?
    - Use format directive names by default and only use human names if
      `humanize=True`?

- Use `surrogateescape` error handling for decoding strings?
    - Without a non-fatal decoding error handler, strings are best left as
      `bytes`.
    - Default to returning bytes but let the user specify an encoding and error
      handler?

- People are likely to copy & paste Apache log formats directly from Apache
  config files, and thus they will likely contain escaped double-quotes.  Does
  this need special handling?

- Handle bytes input? (in Python 2, at least)
    - What encoding are Apache logs written in?  Always ASCII?

- `match` functions should ignore trailing newlines
- Add variants of the `match` functions that match as much as possible from the
  beginning of the string and include whatever didn't match in the results?

- Format directives like `%{*}C` and `%{*}i` that print a value from an
  unrestricted namespace (i.e., not directives like `%{*}T` that can only take
  a fixed set of values for the `*`) should be represented in the result dict
  by sub-dictionaries.

- Aggregate all time fields into a single structure?

- Include instructions in the documentation for adding your own format
  directives (including `%{*}t` sub-directives)
