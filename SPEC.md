- `apachelogs.format` — contains string (and compiled `LogEntryParser`?)
  constants for common, combined, etc.  formats
- `compile(format: str, humanize=False) -> LogEntryParser`
- `LogEntryParser` (`ApacheLogParser`?)
    - `match(entry: str) -> dict`
- `match(format, entry, humanize=False) -> dict`
- `match_lines(format, entries: Iterator[str], humanize=False) -> Iterator[dict]`
- `apachelogs2json [--format <format>] [<file> ...]`
    - The special names "combined" and "common" (et alii?) are accepted as
      formats.
        - Accept these in the library interface as well?
    - Default format: combined?  Guess at combined or common?
- `ValueError` subclass for invalid log formats
- `ValueError` subclass for invalid log entries

s/match/parse/ ?

- If the same format specifier (or two different specifiers with the same name,
  e.g., `%B` and `%b`?) appears more than once in a format, the capturing
  groups for the non-initial occurrences will have their names suffixed with
  `_2`, `_3`, etc.

- Give the `match` functions a way to return a dict that uses the format
  specifiers instead of custom names as keys?
    - Use format specifier names by default and only use human names if
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

- Handle format specifiers that filter by status code
- Handle `<` and `>` modifiers for internally-redirected requests

- `match` functions should ignore trailing newlines
- Add variants of the `match` functions that match as much as possible from the
  beginning of the string and include whatever didn't match in the results?

- Also look into Nginx logfile formats
