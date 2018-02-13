from   collections import namedtuple
from   .util       import unescape

FieldType = namedtuple('FieldType', 'regex converter')

def clf(ftype):
    return FieldType(
        regex=r'(?:-|{})'.format(ftype.regex),
        converter=lambda s: None if s == '-' else ftype.converter(s),
    )

BYTE   = r'(?:[1-9]?[0-9]|[1-9][0-9][0-9]|2[0-4][0-9]|25[0-5])'
HEXTET = r'[0-9A-Fa-f]{1,4}'
IPv4   = r'{BYTE}(?:\.{BYTE}){{3}}'.format(BYTE=BYTE)

IP_ADDRESS_RGX = r'''
    {IPv4}
    # Adapted from <https://git.io/vFxQW>:
    |({HEXTET}:){{7}}({HEXTET}|:)
    |({HEXTET}:){{6}}(:{HEXTET}|{IPv4}|:)
    |({HEXTET}:){{5}}((:{HEXTET}){{1,2}}|:{IPv4}|:)
    |({HEXTET}:){{4}}((:{HEXTET}){{1,3}}|(:{HEXTET})?:{IPv4}|:)
    |({HEXTET}:){{3}}((:{HEXTET}){{1,4}}|(:{HEXTET}){{0,2}}:{IPv4}|:)
    |({HEXTET}:){{2}}((:{HEXTET}){{1,5}}|(:{HEXTET}){{0,3}}:{IPv4}|:)
    |({HEXTET}:){{1}}((:{HEXTET}){{1,6}}|(:{HEXTET}){{0,4}}:{IPv4}|:)
    |:((:{HEXTET}){{1,7}}|(:{HEXTET}){{0,5}}:{IPv4}|:)
'''.format(HEXTET=HEXTET, IPv4=IPv4)

ip_address = FieldType(IP_ADDRESS_RGX, str)
integer    = FieldType(r'(?:0|-?[1-9][0-9]*)', int)
#log_string = FieldType(r'.*?', str)

# The following characters are escaped in logfiles: ", \, control characters
# (whatever matches `apr_iscntrl`), bytes over 127 (whatever fails
# `apr_isprint`?)
# cf. server/gen_test_char.c
### TODO: Accept raw tabs?
### TODO: Accept characters that should be escaped but aren't?
esc_string = FieldType(
    r'(?:[ !\x23-\x5B\x5D-\x7E]|\\x[0-9A-Fa-f]{2}|\\.)*?',
    unescape,
)

clf_string = clf(esc_string)

# A remote user with an empty name is represented by '""' (two double-quotes):
remote_user = FieldType(
    clf_string.regex,
    lambda s: clf_string.converter('' if s == '""' else s),
)
