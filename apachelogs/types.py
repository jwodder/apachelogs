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
log_string = FieldType(r'.*?', str)

# The following characters are escaped in logfiles: ", \, control
# characters (whatever matches `apr_iscntrl`), bytes over 127 (whatever
# fails `apr_isprint`?)
# cf. server/gen_test_char.c
### TODO: Accept characters that should be escaped but aren't?
esc_string = FieldType(r'(?:[^"\\ ??? ] | \\x[0-9A-Fa-f]|\\.)*?', unescape)

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
