import attr

class Error(Exception):
    pass


@attr.s(repr=False, frozen=True)
class InvalidEntryError(Error, ValueError):
    entry      = attr.ib()
    log_format = attr.ib()

    def __str__(self):
        return 'Could not match log entry {0.entry!r}'\
               ' against log format {0.log_format!r}'.format(self)


@attr.s(repr=False, frozen=True)
class InvalidDirectiveError(Error, ValueError):
    directive = attr.ib()

    def __str__(self):
        return 'Invalid/unrecognized log format directive: {!r}'\
            .format(self.directive)
