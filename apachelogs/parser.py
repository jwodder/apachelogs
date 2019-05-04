import re
import attr
from   .directives import format2regex
from   .errors     import InvalidEntryError
from   .util       import assemble_datetime

@attr.s
class LogParser:
    log_format = attr.ib()
    encoding   = attr.ib(default=None)
    errors     = attr.ib(default=None)

    def __attrs_post_init__(self):
        self._group_defs, self._rgx = format2regex(self.log_format)
        self._rgx = re.compile(self._rgx)

    def parse(self, entry):
        entry = entry.rstrip('\r\n')
        m = self._rgx.fullmatch(entry)
        if not m:
            raise InvalidEntryError(entry, self.log_format)
        groups = [
            conv(gr) for (_, _, conv), gr in zip(self._group_defs, m.groups())
        ]
        if self.encoding is not None:
            groups = [
                gr.decode(self.encoding, self.errors or 'strict')
                    if isinstance(gr, bytes)
                    else gr
                for gr in groups
            ]
        return LogEntry(entry, [gdef[:2] for gdef in self._group_defs], groups)

    def parse_lines(self, entries, ignore_invalid=False):
        for e in entries:
            try:
                yield self.parse(e)
            except InvalidEntryError:
                if not ignore_invalid:
                    raise


class LogEntry:
    def __init__(self, entry, group_names, groups):
        self.entry = entry
        for (k,_), v in zip(group_names, groups):
            d = self.__dict__
            if isinstance(k, tuple):
                for k2 in k[:-1]:
                    d = d.setdefault(k2, {})
                k = k[-1]
            if d.get(k) is None:
                d[k] = v
            #else: Assume d[k] == v
        if getattr(self, "time_fields", None):
            self.request_time = assemble_datetime(self.time_fields)

    def __eq__(self, other):
        return type(self) is type(other) and vars(self) == vars(other)
