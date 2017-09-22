# http://httpd.apache.org/docs/current/mod/mod_log_config.html

from collections import namedtuple

BYTE = r'(?:[1-9]?[0-9]|[1-9][0-9][0-9]|2[0-4][0-9]|25[0-5])'
### TODO: Support IPv6:
IP_ADDRESS_RGX = r'{BYTE}(?:\.{BYTE}){{3}}'.format(BYTE=BYTE)

FieldType = namedtuple('FieldType', 'regex converter')

def clf(ftype):
    return FieldType(
        regex=r'(?:-|{})'.format(ftype.regex),
        converter=lambda s: None if s == '-' else ftype.converter(s),
    )

ip_address = FieldType(IP_ADDRESS_RGX, str)
integer = FieldType(r'(?:0|[1-9][0-9]*)', int)
log_string = FieldType(r'.*', str)

# The following characters are escaped in logfiles: ", \, control
# characters (whatever matches `apr_iscntrl`), bytes over 127 (whatever
# fails `apr_isprint`?)
# cf. server/gen_test_char.c
esc_string = FieldType(r'(?:[^"\\ ??? ] | \\x[0-9A-Fa-f]|\\.)*', unescape)


FORMAT_DIRECTIVES = {
    '%': (None, FieldType('%', None)),
    'a': ('remote_ip', ip_address),
    'A': ('local_ip', ip_address),
    'B': ('response_size', integer),
    'b': ('response_size', clf(integer)),

    '{*}C':

    'D': ('microseconds', integer),

    '{*}e':

    'f': ('filename', ??? ),
    'h': ('remote_host', ??? ),
    'H': ('protocol', ??? ),

    '{*}i': ('request_header_*', esc_string),

    'k': ('keepalive', integer),
    'l': ('ident', clf( ??? )), ### Rethink name; remote_logname? ident_logname? ident_user?
    'm': ('method', ??? ),
    '{*}n': ('note_*', ??? ),
    '{*}o': ('response_header_*', esc_string),
    'p': ('port', integer),
    '{*}p': {
        'canonical': ('canonical_port', integer),
        'local': ('local_port', integer),
        'remote': ('remote_port', integer),
    },
    'P': ('pid', integer),
    '{*}P': {
        'pid': ('pid', integer),
        'tid': ('tid', integer),
        'hextid': ('hextid', ???),
    },
    'q': ('query', ???),
    'r': ('request', esc_string),
    'R': ('handler', ???),
    's': ('status', integer),  ### Can this ever be "-"?
    't': ('time', ### Apache timestamp ),
    '{*}t': ???
    'T': ('seconds', integer),  ### float?
    '{*}T': {
        'ms': ('milliseconds', ???),
        'us': ('microseconds', ???),
        's': ('seconds', ???),
    },
    'u': ('remote_user', clf( ??? )),  ### "auth_user"?
    'U': ('path', ???),
    'v': ('server_name', ???),
    'V': ('canonical_server_name', ???),  ### Rethink name
    'X': ('connection_status', FieldType('[-+X]', str)),
    'I': ('bytes_received', integer),  ### CLF?
    'O': ('bytes_sent', integer),  ### CLF?
    '{*}^ti': ('request_trailer_line_*', ???),
    '{*}^to': ('response_trailer_line_*', ???),


### cf. the log definitions shipped with Apache under Ubuntu (Debian?), which
### use %O instead of %b
COMMON_LOG_FORMAT = "%h %l %u %t \"%r\" %>s %b"
COMMON_LOG_VHOST_FORMAT = "%v %h %l %u %t \"%r\" %>s %b"
COMBINED_LOG_FORMAT = "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\""
REFERER_LOG_FORMAT = "%{Referer}i -> %U"
AGENT_LOG_FORMAT = "%{User-agent}i"


def unescape(s):
    # Escape sequences used by Apache: \b \n \r \t \v \\ \" \xHH
    # cf. ap_escape_logitem() in server/util.c
    return re.sub(r'\\(x[0-9A-Fa-f]{2}|.)', _unesc, s)

_unescapes = {
    't': '\t',
    'n': '\n',
    'r': '\r',
    'b': '\b',
    'v': '\v',
    # Not emitted by Apache (as of v2.4), but other servers might use it:
    'f': '\f',
}

def _unesc(m):
    esc = m.group(1)
    if esc[0] == 'x':
        return unichr(int(esc[1:], 16))
    else:
        return _unescapes.get(esc, esc)
