import re

PLAIN_DIRECTIVES = {
    '%': (None, FieldType('%', None)),
    'a': ('remote_address', ip_address),
    'A': ('local_address', ip_address),
    'b': ('bytes_sent', clf(integer)),
    'B': ('bytes_sent', integer),
    'D': ('request_duration_microseconds', integer),
    'f': ('request_file', esc_string),
    'h': ('remote_host', esc_string),
    'H': ('request_protocol', clf(esc_string)),
    'k': ('requests_on_connection', integer),
    'l': ('remote_logname', clf(esc_string)),
    'L': ('log_id', clf( ??? )),
    'm': ('request_method', clf(esc_string)),
    'p': ('server_port', integer),
    'P': ('pid', integer),
    'q': ('request_query', esc_string),
    'r': ('request_line', clf(esc_string)),
    'R': ('handler', esc_string),
    's': ('status', clf(integer)),
    't': ('request_time', ### Apache timestamp ),
    'T': ('request_duration_seconds', integer),
    'u': ('remote_user', clf(esc_string)),
        ### XXX: A user with an empty name is represented by '""' (two
        ### double-quotes)
    'U': ('request_uri', clf(esc_string)),
    'v': ('virtual_host', esc_string),
    'V': ('server_name', esc_string),
    'X': ('connection_status', FieldType('[-+X]', str)),

    # Defined by mod_logio:
    'I': ('bytes_in', integer),  ### Format: apr_off_t_toa
    'O': ('bytes_out', integer),      ### Format: apr_off_t_toa
    'S': ('bytes_combined', integer),  ### Format: apr_off_t_toa
    '^FB': ('ttfb', clf(integer)),
}

PARAMETERIZED_DIRECTIVES = {
    'a': {
        'c': ('remote_client_address', ip_address),
    },
    'C': ('cookie', ???),
    'e': ('env_var', esc_string),
    'i': ('header_in', clf(esc_string)),
    'n': ('note', esc_string),
    'o': ('header_out', esc_string),
    'p': {
        'canonical': ('server_port', integer),
        'local': ('local_port', integer),
        'remote': ('remote_port', integer),
    },
    'P': {
        'pid': ('pid', integer),
        'tid': ('tid', integer),  ### apr_psprintf "%pT" format
        'hextid': ('tid', ???),
            ### apr_psprintf "%pt" or "%pT" format (depending on APR version)
    },
    't': ('request_time', ??? ),
    'T': {
        'ms': ('request_duration_milliseconds', integer),
        'us': ('request_duration_microseconds', integer),
        's': ('request_duration_seconds', integer),
    },
    '^ti': ('trailer_in', esc_string),
    '^to': ('trailer_out', esc_string),
}

def format2regex(fmt, plain_directives=None, parameterized_directives=None):
    if plain_directives is None:
        plain_directives = PLAIN_DIRECTIVES
    if parameterized_directives is None:
        parameterized_directives = PARAMETERIZED_DIRECTIVES
    groups = []
    rgx = ''
    for m in re.finditer(r'''
        % (?:!?\d+(?:,\d+)*)? (?:\{(?P<param>.*?)\})? (?P<directive>\^..|.)
        | (?P<literal>.)
    ''', fmt, flags=re.X):
        if m.group('literal') is not None:
            if m.group('literal') == '%':
                raise InvalidFormatError(fmt)
            rgx += re.escape(m.group('literal'))
            continue
        elif m.group('param') is not None:
            spec = parameterized_directives[m.group('directive')]
            param = m.group('param')
            if isinstance(spec, dict):
                name = (spec[param][0],)
                dtype = spec[param][1]
            else:
                name = (spec[0], param)
                dtype = spec[1]
        else:
            name, dtype = plain_directives[m.group('directive')]
        if name is None:
            rgx += dtype.regex
        else:
            groups.append((name, m.group(0)))
            rgx += r'({})'.format(dtype.regex)
    return (groups, re.compile(rgx))
