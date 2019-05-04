- contains string (and compiled `LogParser`?) constants for common, combined,
  etc. formats
- `LogParser(format: str)`
    - `parse(entry: str) -> LogEntry`
    - `parse_lines(entries: Iterator[str], ignore_invalid=False) -> Iterator[LogEntry]`
- `LogEntry` — represents a parsed log entry
    - Log entry directives are available as attributes of the `LogEntry`
    - Format directives like `%{*}C` and `%{*}i` that print a value from an
      unrestricted namespace (i.e., not directives like `%{*}T` that can only
      take a fixed set of values for the `*`) are represented in the `LogEntry`
      by `dict` attributes
    - If there were any date or time values in the log entry, the `LogEntry`
      instance will have a `request_time` attribute containing a `datetime`
      value (or `None` if there is insufficient data to assemble a `datetime`)
    - All `%t` and `%{*}t` fields are stored (primitively-typed) in a
      `log_entry.time_fields` (`request_time_fields`?) `dict` in order to
      reduce clutter in the main mapping.
    - also supplies a dict with the raw directive strings themselves as keys
      somehow
        - Subfields of `%{*}t` directives can (must?) be accessed with keys of
          the form `"%{%a}t"`
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

- Directives that can contain escape sequences are decoded as Latin-1 by
  default; this can be overridden via the `encoding` argument to `LogParser`.
  Setting `encoding='bytes'` will cause the directive strings to be returned as
  `bytes`.

- `parse` functions should ignore trailing newlines
