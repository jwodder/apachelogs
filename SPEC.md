- contains string (and compiled `LogFormat`?) constants for common, combined,
  etc. formats
- `LogFormat(format: str)`
    - `parse(entry: str) -> LogEntry`
    - `parse_lines(entries: Iterator[str]) -> Iterator[LogEntry]`
- `LogEntry` — represents a parsed log entry
    - can be used as a `dict` with humanized directive names as keys
        - Omit individual timestamp fields from this `dict` so as to reduce
          clutter?
    - also supplies a dict with the raw directive strings themselves as keys
      somehow
        - Subfields of `%{*}t` directives can (must?) be accessed with keys of
          the form `"%{%a}t"`
    - stringifies to the original entry? (possibly with trailing whitespace
      removed)
    - Subdicts for HTTP headers (et alii?) are case-insensitive
- `parse(fmt, entry) -> LogEntry`
- `parse_lines(fmt, entries: Iterator[str]) -> Iterator[LogEntry]`
- `ValueError` subclass for invalid log format directives
- `ValueError` subclass for invalid/non-matching log entries
- Console script: `apachelogs2json [--format <format>] [<file> ...]`
    - The special names "combined" and "common" (et alii?) are accepted as
      formats.
        - Accept these in the library interface as well?
    - Default format: combined?  Guess at combined or common?

- If the same format directive (or two different directives with the same name,
  e.g., `%B` and `%b`) appears more than once in a format, it is assumed that
  the field's value remains constant throughout each individual record, and
  thus all but one of the occurrences (the first? the last?) are discarded

- People are likely to copy & paste Apache log formats directly from Apache
  config files, and thus they will likely contain escaped double-quotes.  Does
  this need special handling?

- Default to returning bytes but let the user specify an encoding and error
  handler (but where?)
    - Or should all input be decoded as Latin-1 by default?

- `parse` functions should ignore trailing newlines

- Add variants of the `parse` functions that match as much as possible from the
  beginning of the string and include whatever didn't match in the results?

- Format directives like `%{*}C` and `%{*}i` that print a value from an
  unrestricted namespace (i.e., not directives like `%{*}T` that can only take
  a fixed set of values for the `*`) should be represented in the result dict
  by sub-dictionaries.

- Aggregate all time fields into a single structure?

- Include instructions in the documentation for adding your own format
  directives (including `%{*}t` sub-directives)
