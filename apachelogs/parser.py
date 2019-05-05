import re
import attr
from   .directives import format2regex
from   .errors     import InvalidEntryError
from   .util       import assemble_datetime

@attr.s
class LogParser:
    """
    A class for parsing Apache access log entries in a given log format.
    Instantiate with a log format string, and then use the `~LogParser.parse()`
    and/or `~LogParser.parse_lines()` methods to parse log entries in that
    format.

    :param str format: an Apache log format
    :param str encoding: The encoding to use for decoding certain strings in
        log entries (see :ref:`directives`); defaults to ``'iso-8859-1'``.  Set
        to ``'bytes'`` to cause the strings to be returned as `bytes` values
        instead of `str`.
    :param str errors: the error handling scheme to use when decoding; defaults
        to ``'strict'``
    :raises InvalidDirectiveError: if an invalid directive occurs in ``format``
    :raises UnknownDirectiveError: if an unknown directive occurs in ``format``
    """

    format   = attr.ib()
    encoding = attr.ib(default='iso-8859-1')
    errors   = attr.ib(default=None)

    def __attrs_post_init__(self):
        self._group_defs, self._rgx = format2regex(self.format)
        self._rgx = re.compile(self._rgx)

    def parse(self, entry):
        """
        Parse an access log entry according to the log format and return a
        `LogEntry` object.

        :param str entry: an access log entry to parse
        :rtype: LogEntry
        :raises InvalidEntryError: if ``entry`` does not match the log format
        """
        entry = entry.rstrip('\r\n')
        m = self._rgx.fullmatch(entry)
        if not m:
            raise InvalidEntryError(entry, self.format)
        groups = [
            conv(gr) for (_, _, conv), gr in zip(self._group_defs, m.groups())
        ]
        if self.encoding != 'bytes':
            groups = [
                gr.decode(self.encoding, self.errors or 'strict')
                    if isinstance(gr, bytes)
                    else gr
                for gr in groups
            ]
        return LogEntry(
            entry,
            self.format,
            [gdef[:2] for gdef in self._group_defs],
            groups,
        )

    def parse_lines(self, entries, ignore_invalid=False):
        r"""
        Parse the elements in an iterable of access log entries (e.g., an open
        text file handle) and return a generator of `LogEntry`\s.  If
        ``ignore_invalid`` is `True`, any entries that do not match the log
        format will be silently discarded; otherwise, such an entry will cause
        an `InvalidEntryError` to be raised.

        :param entries: an iterable of `str`
        :param bool ignore_invalid: whether to silently discard entries that do
            not match the log format
        :rtype: `LogEntry` generator
        :raises InvalidEntryError: if an element of ``entries`` does not match
            the log format and ``ignore_invalid`` is `False`
        """
        for e in entries:
            try:
                yield self.parse(e)
            except InvalidEntryError:
                if not ignore_invalid:
                    raise


class LogEntry:
    """
    A parsed Apache access log entry.  The value associated with each directive
    in the log format is stored as an attribute on the `LogEntry` object; for
    example, if the log format contains a ``%s`` directive, the `LogEntry` for
    a parsed entry will have a ``status`` attribute containing the status value
    from the entry as an `int`.  See :ref:`directives` for the attribute names
    & types of each directive supported by this library.

    If the log format contains two or more directives that are stored in the
    same attribute (e.g., ``%D`` and ``%{us}T``), the given attribute will
    contain the first non-`None` directive value.

    The values of date & time directives are stored in a ``request_time_fields:
    dict`` attribute.  If this `dict` contains enough information to assemble a
    complete (possibly naïve) `datetime.datetime`, then the `LogEntry` will
    have a ``request_time`` attribute equal to that `datetime.datetime`.
    """

    def __init__(self, entry, format, group_names, groups):
        #: The original logfile entry with trailing newlines removed
        self.entry = entry
        #: The entry's log format string
        self.format = format
        for (k,_), v in zip(group_names, groups):
            d = self.__dict__
            if isinstance(k, tuple):
                for k2 in k[:-1]:
                    d = d.setdefault(k2, {})
                k = k[-1]
            if d.get(k) is None:
                d[k] = v
            #else: Assume d[k] == v
        if getattr(self, "request_time_fields", None):
            self.request_time = assemble_datetime(self.request_time_fields)

    def __eq__(self, other):
        return type(self) is type(other) and vars(self) == vars(other)
