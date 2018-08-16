import pyparsing as P
from   pyparsing import pyparsing_common as PC
from   .util     import CLF_NULL_TOKEN, unescape

def clf(p):
    return (p | P.Literal("-")).setParseAction(
        lambda toks: CLF_NULL_TOKEN if len(toks) == 1 and toks[0] in ("-", b"-") else None
    )

ip_address = PC.ipv4_address ^ PC.ipv6_address

# The following characters are escaped in logfiles: ", \, control characters
# (whatever matches `apr_iscntrl`), bytes over 127 (whatever fails
# `apr_isprint`?)
# cf. server/gen_test_char.c
### TODO: Accept raw tabs?
### TODO: Accept characters that should be escaped but aren't?
esc_string = P.ZeroOrMore(
    P.Word(P.printables, excludeChars='"\\', exact=1)
    | (r'\x' + P.Word(P.hexnums, exact=2))
    | (r'\\' + P.Word(P.alphas + '"\\', exact=1))
).setParseAction(lambda toks: unescape(''.join(toks)))

clf_string = clf(esc_string)

# A remote user with an empty name is represented by '""' (two double-quotes):
remote_user = clf_string.addParseAction(
    lambda toks: '' if toks[0] == '""' else toks
)
