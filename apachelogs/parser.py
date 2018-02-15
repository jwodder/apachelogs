from   collections.abc import Mapping
import attr
from   .directives     import format2regex
from   .errors         import InvalidEntryError
from   .util           import TIME_FIELD_TOKEN, assemble_datetime

@attr.s
class LogFormat:
    log_format = attr.ib()
    encoding   = attr.ib(default=None)
    errors     = attr.ib(default=None)

    def __attrs_post_init__(self):
        self._group_defs, self._rgx = format2regex(self.log_format)

    def parse(self, entry):
        if isinstance(entry, bytes):
            entry = entry.decode('us-ascii')
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

    def parse_lines(self, entries):
        for e in entries:
            yield self.parse(e)


@attr.s
class LogEntry(Mapping):
    entry = attr.ib()
    group_names = attr.ib()
    groups = attr.ib()

    def __attrs_post_init__(self):
        self._data = {}
        self.time_fields = {}
        for (k,_), v in zip(self.group_names, self.groups):
            d = self._data
            if isinstance(k, tuple):
                for k2 in k[:-1]:
                    if k2 is TIME_FIELD_TOKEN:
                        d = self.time_fields
                    else:
                        d = d.setdefault(k2, {})
                k = k[-1]
            if d.get(k) is None:
                d[k] = v
            #else: Assume d[k] == v
        if self.time_fields:
            self._data["request_time"] = assemble_datetime(self.time_fields)

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        return key in self._data
