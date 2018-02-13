import re
from   .errors import InvalidDirectiveError
from   .types  import (FieldType, clf, clf_string, esc_string, integer,
                       ip_address, remote_user)
from   .util   import parse_apache_timestamp

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
    'q': ('request_query', esc_string),
    'r': ('request_line', clf_string),
    'R': ('handler', esc_string),
    's': ('status', clf(integer)),
    't': ('request_time', FieldType(r'\[[^]]+\]', parse_apache_timestamp)),
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
    'C': ('cookie', esc_string),
    'e': ('env_var', esc_string),
    'i': ('header_in', clf_string),
    'n': ('note', esc_string),
    'o': ('header_out', esc_string),
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
    ### XXX: 't': ('request_time', ??? ),  ### strftime
    'T': {
        'ms': ('request_duration_milliseconds', integer),
        'us': ('request_duration_microseconds', integer),
        's': ('request_duration_seconds', integer),
    },
    '^ti': ('trailer_in', esc_string),
    '^to': ('trailer_out', esc_string),
}

#STRFTIME_DIRECTIVES = {
#    '%': (None, FieldType('%', None)),
#    's': ('unix', integer),
#    'w': ('wday', FieldType(r'[0-6]', int)),
#    'u': ('iso_wday', FieldType(r'[1-7]', int)),
#    'm': ('mon',
#    'd': ('mday',
#    'A': ('full_wday',
#    'B': ('full_mon',
#    'a': ('abbrev_wday',
#    'b': ('abbrev_mon',
#    'Y': ('year',
#    'C': ('century',
#    'y': ('abbrev_year',
#    ???
#}

def format2regex(fmt, plain_directives=None, parameterized_directives=None):
    if plain_directives is None:
        plain_directives = PLAIN_DIRECTIVES
    if parameterized_directives is None:
        parameterized_directives = PARAMETERIZED_DIRECTIVES
    groups = []
    rgx = ''
    for m in re.finditer(r'''
        % (?:!?\d+(?:,\d+)*|(?P<redirect1>[<>]))*
          (?:\{(?P<param>.*?)\})?
          (?:!?\d+(?:,\d+)*|(?P<redirect2>[<>]))*
          (?P<directive>\^..|.)
        | (?P<literal>.)
    ''', fmt, flags=re.X):
        if m.group('literal') is not None:
            if m.group('literal') == '%':
                raise InvalidDirectiveError(m.group(0))
            rgx += re.escape(m.group('literal'))
            continue
        try:
            if m.group('param') is not None:
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
        except KeyError:
            raise InvalidDirectiveError(m.group(0))
        if name is None:
            rgx += dtype.regex
        else:
            redirect = m.group('redirect2') or m.group('redirect1') or ''
            if redirect == '<':
                name = 'original_' + name
            elif redirect == '>':
                name = 'final_' + name
            groups.append((name, m.group(0), dtype.converter))
            rgx += r'({})'.format(dtype.regex)
    return (groups, re.compile(rgx))
