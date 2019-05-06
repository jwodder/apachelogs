from   collections import namedtuple
from   .util       import unescape

#: `collections.namedtuple` class for describing how to match various types and
#: how to convert them from strings.  The two attributes are ``regex``, a regex
#: string, and ``converter``, a function that takes a `str` and returns an
#: value of the appropriate type.
FieldType = namedtuple('FieldType', 'regex converter')

def clf(ftype):
    """
    Convert a `FieldType` instance to one whose ``regex`` accepts the string
    ``-`` and whose ``converter`` converts the string ``-`` to `None`

    :param FieldType ftype:
    :rtype: FieldType
    """
    return FieldType(
        regex=r'(?:{}|-)'.format(ftype.regex),
        converter=lambda s: None if s == '-' else ftype.converter(s),
    )

#: Regex matching a base-10 integer from 0 to 255
BYTE   = r'(?:[1-9]?[0-9]|[1-9][0-9][0-9]|2[0-4][0-9]|25[0-5])'

#: Regex matching one to four hexadecimal digits
HEXTET = r'[0-9A-Fa-f]{1,4}'

#: Regex for an IPv4 address
IPv4   = r'{BYTE}(?:\.{BYTE}){{3}}'.format(BYTE=BYTE)

#: Regex for an IP address, either IPv4 or IPv6
IP_ADDRESS_RGX = (
    '{IPv4}'
    # Adapted from <https://git.io/vFxQW>:
    '|(?:{HEXTET}:){{7}}(?:{HEXTET}|:)'
    '|(?:{HEXTET}:){{6}}(?::{HEXTET}|{IPv4}|:)'
    '|(?:{HEXTET}:){{5}}(?:(?::{HEXTET}){{1,2}}|:{IPv4}|:)'
    '|(?:{HEXTET}:){{4}}(?:(?::{HEXTET}){{1,3}}|(?::{HEXTET})?:{IPv4}|:)'
    '|(?:{HEXTET}:){{3}}(?:(?::{HEXTET}){{1,4}}|(?::{HEXTET}){{0,2}}:{IPv4}|:)'
    '|(?:{HEXTET}:){{2}}(?:(?::{HEXTET}){{1,5}}|(?::{HEXTET}){{0,3}}:{IPv4}|:)'
    '|(?:{HEXTET}:){{1}}(?:(?::{HEXTET}){{1,6}}|(?::{HEXTET}){{0,4}}:{IPv4}|:)'
    '|:(?:(?::{HEXTET}){{1,7}}|(?::{HEXTET}){{0,5}}:{IPv4}|:)'
).format(HEXTET=HEXTET, IPv4=IPv4)

#: `FieldType` instance for an IP address, either IPv4 or IPv6
ip_address = FieldType(IP_ADDRESS_RGX, str)

#: `FieldType` instance for a base-10 integer
integer    = FieldType(r'(?:0|-?[1-9][0-9]*)', int)

#log_string = FieldType(r'.*?', str)

#: `FieldType` instance for a string containing escape sequences that is
#: converted to `bytes`
esc_string = FieldType(
    # The following characters are escaped in logfiles: ", \, control
    # characters (whatever matches `apr_iscntrl`), bytes over 127 (whatever
    # fails `apr_isprint`?)
    # cf. server/gen_test_char.c
    ### TODO: Accept raw tabs?
    ### TODO: Accept characters that should be escaped but aren't?
    r'(?:[ !\x23-\x5B\x5D-\x7E]|\\x[0-9A-Fa-f]{2}|\\.)*?',
    unescape,
)

#: `FieldType` instance for a "Common Log Format" string: either a string with
#: escape sequences or else a single hyphen, representing `None`
clf_string = clf(esc_string)

#: `FieldType` instance for a remote user (directive ``%u``).  This is the same
#: as `clf_string`, but the converter additionally converts ``""`` (two
#: double-quotes) to an empty string, as that is how ``%u`` represents empty
#: names.
remote_user = FieldType(
    clf_string.regex,
    lambda s: clf_string.converter('' if s == '""' else s),
)
