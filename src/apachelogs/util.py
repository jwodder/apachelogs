from   collections import namedtuple
import re

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
        regex=fr'(?:{ftype.regex}|-)',
        converter=lambda s: None if s == '-' else ftype.converter(s),
    )

def unescape(s):
    """
    Unescape the escape sequences in the string ``s``, returning a `bytes`
    string
    """
    # Escape sequences used by Apache: \b \n \r \t \v \\ \" \xHH
    # cf. ap_escape_logitem() in server/util.c
    return re.sub(r'\\(x[0-9A-Fa-f]{2}|.)', _unesc, s).encode('iso-8859-1')

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
        return chr(int(esc[1:], 16))
    else:
        return _unescapes.get(esc, esc)

#: Regex matching a base-10 integer from 0 to 255
BYTE   = r'(?:[1-9]?[0-9]|[1-9][0-9][0-9]|2[0-4][0-9]|25[0-5])'

#: Regex matching one to four hexadecimal digits
HEXTET = r'[0-9A-Fa-f]{1,4}'

#: Regex for an IPv4 address
IPv4   = fr'{BYTE}(?:\.{BYTE}){{3}}'

#: Regex for an IP address, either IPv4 or IPv6
IP_ADDRESS_RGX = (
    f'{IPv4}'
    # Adapted from <https://git.io/vFxQW>:
    f'|(?:{HEXTET}:){{7}}(?:{HEXTET}|:)'
    f'|(?:{HEXTET}:){{6}}(?::{HEXTET}|{IPv4}|:)'
    f'|(?:{HEXTET}:){{5}}(?:(?::{HEXTET}){{1,2}}|:{IPv4}|:)'
    f'|(?:{HEXTET}:){{4}}(?:(?::{HEXTET}){{1,3}}|(?::{HEXTET})?:{IPv4}|:)'
    f'|(?:{HEXTET}:){{3}}(?:(?::{HEXTET}){{1,4}}|(?::{HEXTET}){{0,2}}:{IPv4}|:)'
    f'|(?:{HEXTET}:){{2}}(?:(?::{HEXTET}){{1,5}}|(?::{HEXTET}){{0,3}}:{IPv4}|:)'
    f'|(?:{HEXTET}:){{1}}(?:(?::{HEXTET}){{1,6}}|(?::{HEXTET}){{0,4}}:{IPv4}|:)'
    f'|:(?:(?::{HEXTET}){{1,7}}|(?::{HEXTET}){{0,5}}:{IPv4}|:)'
)

#: `FieldType` instance for an IP address, either IPv4 or IPv6
ip_address = FieldType(IP_ADDRESS_RGX, str)

#: `FieldType` instance for a base-10 integer
integer    = FieldType(r'(?:0|-?[1-9][0-9]*)', int)

#: `FieldType` instance for an unsigned base-10 integer
uinteger   = FieldType(r'(?:0|[1-9][0-9]*)', int)

#: `FieldType` instance for a 3-digit integer HTTP status code
status_code = FieldType(r'[0-9]{3}', int)

#: `FieldType` instance for a string containing escape sequences that is
#: converted to `bytes`
esc_string = FieldType(
    # The following characters are escaped in logfiles: ", \, control
    # characters (everything accepted by `apr_iscntrl` = `iscntrl`, i.e.,
    # everything less than 0x20 and also 0x7F), non-printable characters
    # (everything rejected by `apr_isprint` = `isprint`, i.e., control
    # characters plus everything over 0x7F).
    # cf. server/gen_test_char.c
    r'(?:[ !\x23-\x5B\x5D-\x7E]|\\x[0-9A-Fa-f]{2}|\\.)*?',
    unescape,
)

#: Like `esc_string`, but without any whitespace.  (Whitespace escape sequences
#: are still allowed just because it's easier.)
esc_word = FieldType(
    r'(?:[!\x23-\x5B\x5D-\x7E]|\\x[0-9A-Fa-f]{2}|\\.)*?',
    unescape,
)

#: `FieldType` instance for a "Common Log Format" string: either a string with
#: escape sequences or else a single hyphen, representing `None`
clf_string = clf(esc_string)

#: Like `clf_string`, but without any whitespace.  (Whitespace escape sequences
#: are still allowed just because it's easier.)
clf_word = clf(esc_word)

#: `FieldType` instance for a remote user (directive ``%u``).  This is the same
#: as `clf_string`, but ``""`` (two double-quotes) is accepted and converted to
#: an empty string, as that is how ``%u`` represents empty names.
remote_user = FieldType(
    fr'(?:{clf_string.regex}|"")',
    lambda s: clf_string.converter('' if s == '""' else s),
)

#: Regex for a single non-space atom in a cookie value; this is the same as an
#: `esc_word` atom, except semicolons are not matched
CRUMB = r'(?:[!\x23-\x3A\x3C-\x5B\x5D-\x7E]|\\x[0-9A-Fa-f]{2}|\\.)'

#: `FieldType` instance for a cookie value; like `clf_string`, but with no
#: leading or trailing spaces and no semicolons
cookie_value = clf(FieldType(
    fr'{CRUMB}(?:(?:{CRUMB}|[ ])*{CRUMB})?',
    unescape,
))
