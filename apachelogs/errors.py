class Error(Exception):
    """ The base class for all custom exceptions raised by ``apachelogs`` """
    pass


class InvalidEntryError(Error, ValueError):
    """
    Raised when a attempting to parse a log entry that does not match the given
    log format
    """

    def __init__(self, entry, log_format):
        #: The invalid log entry
        self.entry      = entry
        #: The log format string the entry failed to match against
        self.log_format = log_format

    def __str__(self):
        return 'Could not match log entry {0.entry!r}'\
               ' against log format {0.log_format!r}'.format(self)


class InvalidDirectiveError(Error, ValueError):
    """
    Raised by the `LogParser` constructor when given a log format containing an
    invalid or malformed directive
    """

    def __init__(self, log_format, pos):
        #: The log format string containing the invalid directive
        self.log_format = log_format
        #: The position in the log format string at which the invalid directive
        #: occurs
        self.pos = pos

    def __str__(self):
        return 'Invalid log format directive at column {} of {!r}'\
            .format(self.pos, self.log_format)


class UnknownDirectiveError(Error, ValueError):
    """
    Raised by the `LogParser` constructor when given a log format containing an
    unknown or unsupported directive
    """

    def __init__(self, directive):
        #: The unknown or unsupported directive
        self.directive = directive

    def __str__(self):
        return 'Unknown log format directive: {!r}'.format(self.directive)
