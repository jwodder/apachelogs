import re
from   pydicti   import dicti
from   .errors   import InvalidDirectiveError, UnknownDirectiveError
from   .strftime import strftime2regex
from   .timeutil import parse_apache_timestamp
from   .util     import (FieldType, clf, clf_string, clf_word, cookie_value,
                         esc_string, integer, ip_address, remote_user,
                         status_code, uinteger, unescape)

PLAIN_DIRECTIVES = {
    '%': (None, FieldType('%', None)),
    'a': ('remote_address', ip_address),
    'A': ('local_address', ip_address),
    'b': ('bytes_sent', clf(integer)),
    'B': ('bytes_sent', integer),
    'D': ('request_duration_microseconds', integer),
    # `%f` is '-' for malformed requests.
    'f': ('request_file', clf_string),
    'h': ('remote_host', esc_string),
    # In some versions of Apache (I think this includes 2.4.18, the version
    # available to Xenial), `%H` is everything in the request line from the
    # third word onward, and thus it can be anything.  In some other versions
    # (including 2.4.7, Trusty's version?), `%H` can even be '-' for certain
    # very malformed request lines.
    'H': ('request_protocol', clf_string),
    'k': ('requests_on_connection', integer),
    # As of v2.4.39, Apache uses the `%s` sscanf() format to extract the value
    # that becomes `remote_logname`, and so it does not contain any whitespace.
    'l': ('remote_logname', clf_word),
    # `%L` is the base64-encoding of a byte sequence with trailing '=' removed.
    # Depending on whether mod_unique_id is loaded, the encoding will use
    # either '+' and '/' or '@' and '-'.
    'L': ('request_log_id', clf(FieldType(r'[-@/+A-Za-z0-9]+', str))),
    # `%m` is the first word of the request line, i.e., it does not contain any
    # whitespace.
    # `%m` is '-' when the request line is malformed.
    'm': ('request_method', clf_word),
    'p': ('server_port', integer),
    'P': ('pid', integer),
    # As of httpd v2.4.29, `%q` is formatted as either an empty string or `?`
    # followed by a (possibly empty, in the case where the requested URI ends
    # with '?') escaped string.  Moreover, due to the way the query string is
    # parsed from the request URI, it will never contain a '#', and due to the
    # way the request URI is parsed from the request line, `%q` will never
    # contain whitespace.
    'q': (
        'request_query',
        FieldType(
            r'(?:\?(?:[!\x24-\x5B\x5D-\x7E]|\\x[0-9A-Fa-f]{2}|\\.)*?)?',
            unescape,
        )
    ),
    # `%r` is just the first line sent by the client, and so it can be
    # anything.  I've even seen it as '-' in logs, though I can't quite figure
    # out how to reproduce that.
    'r': ('request_line', clf_string),
    'R': ('handler', clf_string),
    # httpd v2.4.29 has a provision in its code for converting statuses less
    # than or equal to zero to "-".  I'm not sure when that can happen, but
    # apparently it can.
    's': ('status', clf(status_code)),
    't': (
        ('request_time_fields', 'timestamp'),
        FieldType(r'\[[^]]+\]', parse_apache_timestamp),
    ),
    'T': ('request_duration_seconds', integer),
    'u': ('remote_user', remote_user),
    # Starting somewhere between versions 2.4.18 and 2.4.29 of Apache (or maybe
    # earlier?), `%U` has (some?) percent-escapes decoded and thus may contain
    # whitespace and '?' (and just about any other ASCII character?).
    # `%U` is '-' when the request line is malformed.
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
    'C': ('cookies', cookie_value),
    'e': ('env_vars', clf_string),
    'h': {
        'c': ('remote_underlying_host', esc_string),
    },
    'i': ('headers_in', clf_string),
    # `%{c}L` is derived the same way as `%L`; see above.
    'L': {
        'c': ('connection_log_id', clf(FieldType(r'[-@/+A-Za-z0-9]+', str))),
    },
    'n': ('notes', clf_string),
    'o': ('headers_out', clf_string),
    'p': dicti({
        'canonical': ('server_port', integer),
        'local': ('local_port', integer),
        'remote': ('remote_port', integer),
    }),
    'P': dicti({
        'pid': ('pid', integer),
        # `%{tid}P` is formatted as an unsigned integer.
        'tid': ('tid', uinteger),
        'hextid': ('tid', FieldType(r'[0-9A-Fa-f]+', lambda s: int(s, 16))),
    }),
    't': strftime2regex,
    'T': dicti({
        'ms': ('request_duration_milliseconds', integer),
        'us': ('request_duration_microseconds', integer),
        's': ('request_duration_seconds', integer),
    }),
    '^ti': ('trailers_in', clf_string),
    '^to': ('trailers_out', clf_string),

    # Defined by mod_ssl:
    # As of Apache 2.4.39, no escaping is performed on the values of `%{*}x`
    # and `%{*}c` despite the fact that they can be just about anything.
    'c': ('cryptography', clf(FieldType(r'.+?', str))),
    'x': ('variables', clf(FieldType(r'.+?', str))),
}

DIRECTIVE_RGX = re.compile(r'''
    % (?P<modifiers1>[0-9,!<>]*)
      (?:\{(?P<param>[^}]*)\})?
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
        modifiers = m.group('modifiers1') + m.group('modifiers2')
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
                            '%' + m.group('modifiers1')
                                + '{' + directive + '}'
                                + m.group('modifiers2')
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
                subrgx = f'(?:{subrgx}|-)'
            rgx += subrgx
        else:
            if name is None:
                rgx += f'(?:{dtype.regex})'
                continue
            if conditioned:
                dtype = clf(dtype)
            rgx += fr'({dtype.regex})'
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
