class Error(Exception):
    pass


class InvalidEntryError(Error, ValueError):
    def __init__(self, entry, log_format):
        self.entry      = entry
        self.log_format = log_format

    def __str__(self):
        return 'Could not match log entry {0.entry!r}'\
               ' against log format {0.log_format!r}'.format(self)


class InvalidDirectiveError(Error, ValueError):
    def __init__(self, log_format, pos):
        self.log_format = log_format
        self.pos = pos

    def __str__(self):
        return 'Invalid log format directive at column {} of {!r}'\
            .format(self.pos, self.log_format)


class UnknownDirectiveError(Error, ValueError):
    def __init__(self, directive):
        self.directive = directive

    def __str__(self):
        return 'Unknown log format directive: {!r}'.format(self.directive)
