from   collections.abc import Mapping
import attr
from   .directives     import format2parser
#from   .errors         import InvalidEntryError
from   .util           import CLF_NULL_TOKEN, TIME_FIELD_TOKEN, assemble_datetime

@attr.s
class LogFormat:
    log_format = attr.ib()
    encoding   = attr.ib(default=None)
    errors     = attr.ib(default=None)

    def __attrs_post_init__(self):
        self._parser = format2parser(self.log_format)

    def parse(self, entry):
        if isinstance(entry, bytes):
            entry = entry.decode('iso-8859-1')
        entry = entry.rstrip('\r\n')
        #try:
        r = self._parser.parseString(entry, parseAll=True)
        #except ... :
        #    raise InvalidEntryError(entry, self.log_format)
        groups = {
            k: None if v is CLF_NULL_TOKEN else v
            for k,v in dict(r).items()
        }
        if self.encoding is not None:
            groups = {
                k: v.decode(self.encoding, self.errors or 'strict')
                    if isinstance(v, bytes)
                    else v
                for k,v in groups.items()
            }
        return LogEntry(entry, groups)

    def parse_lines(self, entries):
        for e in entries:
            yield self.parse(e)


@attr.s
class LogEntry(Mapping):
    entry = attr.ib()
    groups = attr.ib()

    def __attrs_post_init__(self):
        self._data = {}
        self.time_fields = {}
        for k, v in self.groups.items():
            d = self._data
            if ':' in k:
                k1, _, k = k.partition(':')
                if k1 == TIME_FIELD_TOKEN:
                    d = self.time_fields
                else:
                    d = d.setdefault(k1, {})
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
