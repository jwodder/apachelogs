import pyparsing as P
from   pyparsing import pyparsing_common as PC
from   .util     import unescape

def clf(p):
    return (p | P.Literal("-")).setParseAction(
        lambda toks: None if len(toks) == 0 and toks[0] == "-" else toks
    )

ip_address = PC.ipv4_address ^ PC.ipv6_address

# The following characters are escaped in logfiles: ", \, control characters
# (whatever matches `apr_iscntrl`), bytes over 127 (whatever fails
# `apr_isprint`?)
# cf. server/gen_test_char.c
### TODO: Accept raw tabs?
### TODO: Accept characters that should be escaped but aren't?
esc_string = P.Regex(r'(?:[ !\x23-\x5B\x5D-\x7E]|\\x[0-9A-Fa-f]{2}|\\.)*?')\
              .setParseAction(lambda toks: unescape(toks[0]))

clf_string = clf(esc_string)

# A remote user with an empty name is represented by '""' (two double-quotes):
remote_user = clf_string.addParseAction(
    lambda toks: '' if toks[0] == '""' else toks
)
