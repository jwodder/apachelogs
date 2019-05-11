import re
from   .errors   import InvalidDirectiveError, UnknownDirectiveError
from   .strftime import strftime2regex
from   .types    import (FieldType, clf, clf_string, esc_string, integer,
                         ip_address, remote_user)
from   .util     import parse_apache_timestamp

PLAIN_DIRECTIVES = {
    '%': (None, FieldType('%', None)),
    'a': ('remote_address', ip_address),
    'A': ('local_address', ip_address),
    'b': ('bytes_sent', clf(integer)),
    'B': ('bytes_sent', integer),
    'D': ('request_duration_microseconds', integer),
    'f': ('request_file', esc_string),
    'h': ('remote_host', esc_string),
    'H': ('request_protocol', clf_string),
    'k': ('requests_on_connection', integer),
    'l': ('remote_logname', clf_string),
    ### XXX: 'L': ('log_id', clf( ??? )),
    'm': ('request_method', clf_string),
    'p': ('server_port', integer),
    'P': ('pid', integer),
    # As of httpd v2.4.29, `%q` is formatted as either an empty string or `?`
    # followed by an escaped string (`r->args`); see `log_request_query()` in
    # `modules/loggers/mod_log_config.c`.
    'q': (
        'request_query',
        FieldType(r'(?:\?{})?'.format(esc_string.regex), esc_string.converter)
    ),
    'r': ('request_line', clf_string),
    'R': ('handler', esc_string),
    # httpd v2.4.29 has a provision in its code for converting statuses less
    # than or equal to zero to "-".  I'm not sure when that can happen, but
    # apparently it can.
    's': ('status', clf(integer)),
    't': (
        ('request_time_fields', 'timestamp'),
        FieldType(r'\[[^]]+\]', parse_apache_timestamp),
    ),
    'T': ('request_duration_seconds', integer),
    'u': ('remote_user', remote_user),
    'U': ('request_uri', clf_string),
    'v': ('virtual_host', esc_string),
    'V': ('server_name', esc_string),
    'X': ('connection_status', FieldType('[-+X]', str)),

    # Defined by mod_logio:
    'I': ('bytes_in', integer),
    'O': ('bytes_out', integer),
    'S': ('bytes_combined', integer),
    '^FB': ('ttfb', clf(integer)),
}

PARAMETERIZED_DIRECTIVES = {
    'a': {
        'c': ('remote_client_address', ip_address),
    },
    'C': ('cookies', clf_string),
    'e': ('env_vars', clf_string),
    'i': ('headers_in', clf_string),
    'n': ('notes', clf_string),
    'o': ('headers_out', clf_string),
    'p': {
        'canonical': ('server_port', integer),
        'local': ('local_port', integer),
        'remote': ('remote_port', integer),
    },
    'P': {
        'pid': ('pid', integer),
        'tid': ('tid', integer),
        ### XXX: 'hextid': ('tid', ???),  ### decimal or hex integer (depending on APR version)
    },
    't': strftime2regex,
    'T': {
        'ms': ('request_duration_milliseconds', integer),
        'us': ('request_duration_microseconds', integer),
        's': ('request_duration_seconds', integer),
    },
    '^ti': ('trailers_in', clf_string),
    '^to': ('trailers_out', clf_string),
}

DIRECTIVE_RGX = re.compile(r'''
    % (?P<modifiers1>[0-9,!<>]*)
      (?:\{(?P<param>.*?)\})?
      (?P<modifiers2>[0-9,!<>]*)
      (?P<directive>\^[a-zA-Z%]{2}|[a-zA-Z%])
    | (?P<literal>.)
''', flags=re.X)

def format2regex(fmt, plain_directives=None, parameterized_directives=None,
                 simple=False):
    """
    Given a %-style format string ``fmt`` made up of a mixture of the "plain"
    directives (e.g., ``%q``) in ``plain_directives`` (default
    `PLAIN_DIRECTIVES`) and the parameterized directives (e.g., ``%{foo}q``) in
    ``parameterized_directives`` (default `PARAMETERIZED_DIRECTIVES`), return a
    pair ``(groups, rgx)`` where:

    - ``groups`` is a list of ``(name, directive, converter)`` triples,
      corresponding to the respective capturing groups in ``rgx``, where:

      - ``name`` is the name (if a `str`) or path (if a `tuple` of `str`) at
        which the converted captured value shall be saved in a `LogEntry`
        instance

      - ``directive`` is the complete directive in ``fmt`` that produced this
        triple and capturing group

      - ``converter`` is a function that takes a `str` (the captured value) and
        returns a value

    - ``rgx`` is a regex string that matches any string created from ``fmt``,
      with a capturing group around the substring corresponding to each
      non-``%%`` directive

    :param str fmt:
    :param dict plain_directives: A `dict` mapping plain directive names to
        ``(name, field_type)`` pairs.  A ``name`` of `None` (as for the ``%%``
        directive) indicates that input text matching the directive shall not
        be captured.
    :param dict parameterized_directives: A `dict` mapping parameterized
        directive names either to a ``(name, field_type)`` pair (where the
        ``name`` is the name of the `dict` attribute of `LogEntry` in which a
        key named after the parameter will store the converted captured value),
        or to a sub-`dict` mapping parameter values to ``(name, field_type)``
        pairs, or to a callable that takes a parameter and returns the same
        return type as `format2regex()`.
    :param bool simple: If `True`, an `InvalidDirectiveError` will be raised if
        a directive with modifiers or a parameter is encountered
    :raises InvalidDirectiveError: if an invalid directive occurs in ``fmt``
    :raises UnknownDirectiveError: if an unknown directive occurs in ``fmt``
    """

    if plain_directives is None:
        plain_directives = PLAIN_DIRECTIVES
    if parameterized_directives is None:
        parameterized_directives = PARAMETERIZED_DIRECTIVES
    groups = []
    rgx = ''
    for m in DIRECTIVE_RGX.finditer(fmt):
        if m.group('literal') is not None:
            if m.group('literal') == '%':
                raise InvalidDirectiveError(fmt, m.start())
            rgx += re.escape(m.group('literal'))
            continue
        multiple = False
        modifiers = (m.group('modifiers1') or '')+(m.group('modifiers2') or '')
        conditioned = any(c.isdigit() for c in modifiers)
        redirects = re.findall(r'[<>]', modifiers)
        if simple and (modifiers or m.group('param') is not None):
            raise InvalidDirectiveError(fmt, m.start())
        try:
            if m.group('param') is not None:
                spec = parameterized_directives[m.group('directive')]
                param = m.group('param')
                if isinstance(spec, dict):
                    name, dtype = spec[param]
                elif callable(spec):
                    subgroups, subrgx = spec(param)
                    subgroups = [
                        (
                            name,
                            '%' + (m.group('modifiers1') or '')
                                + '{' + directive + '}'
                                + (m.group('modifiers2') or '')
                                + m.group('directive'),
                            converter,
                        )
                        for (name, directive, converter) in subgroups
                    ]
                    multiple = True
                else:
                    name = (spec[0], param)
                    dtype = spec[1]
            else:
                name, dtype = plain_directives[m.group('directive')]
        except KeyError:
            raise UnknownDirectiveError(m.group(0))
        if multiple:
            if conditioned:
                subrgx = '(?:{}|-)'.format(subrgx)
            rgx += subrgx
        else:
            if name is None:
                rgx += '(?:{})'.format(dtype.regex)
                continue
            if conditioned:
                dtype = clf(dtype)
            rgx += r'({})'.format(dtype.regex)
            subgroups = [(name, m.group(0), dtype.converter)]
        if redirects:
            prefix = 'original_' if redirects[-1] == '<' else 'final_'
            for i, (name, directive, converter) in enumerate(subgroups):
                if isinstance(name, tuple):
                    name = (prefix + name[0],) + name[1:]
                else:
                    name = prefix + name
                subgroups[i] = (name, directive, converter)
        groups.extend(subgroups)
    return (groups, rgx)
