import pyparsing as P
from   pyparsing import pyparsing_common as PC
from   .errors   import InvalidDirectiveError
from   .types    import clf, clf_string, esc_string, ip_address, remote_user
from   .util     import TIME_FIELD_TOKEN

PLAIN_DIRECTIVES = {
    '%': (None, P.Literal('%')),
    'a': ('remote_address', ip_address),
    'A': ('local_address', ip_address),
    'b': ('bytes_sent', clf(PC.signed_integer)),
    'B': ('bytes_sent', PC.signed_integer),
    'D': ('request_duration_microseconds', PC.signed_integer),
    'f': ('request_file', esc_string),
    'h': ('remote_host', esc_string),
    'H': ('request_protocol', clf_string),
    'k': ('requests_on_connection', PC.signed_integer),
    'l': ('remote_logname', clf_string),
    ### XXX: 'L': ('log_id', clf( ??? )),
    'm': ('request_method', clf_string),
    'p': ('server_port', PC.signed_integer),
    'P': ('pid', PC.signed_integer),
    'q': ('request_query', esc_string),
    'r': ('request_line', clf_string),
    'R': ('handler', esc_string),
    's': ('status', clf(PC.signed_integer)),
    't': (TIME_FIELD_TOKEN + ':apache_timestamp', P.Regex(r'\[[^]]+\]')),
    'T': ('request_duration_seconds', PC.signed_integer),
    'u': ('remote_user', remote_user),
    'U': ('request_uri', clf_string),
    'v': ('virtual_host', esc_string),
    'V': ('server_name', esc_string),
    'X': ('connection_status', P.Word("-+X", exact=1)),

    # Defined by mod_logio:
    'I': ('bytes_in', PC.signed_integer),
    'O': ('bytes_out', PC.signed_integer),
    'S': ('bytes_combined', PC.signed_integer),
    '^FB': ('ttfb', clf(PC.signed_integer)),
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
        'canonical': ('server_port', PC.signed_integer),
        'local': ('local_port', PC.signed_integer),
        'remote': ('remote_port', PC.signed_integer),
    },
    'P': {
        'pid': ('pid', PC.signed_integer),
        'tid': ('tid', PC.signed_integer),
        ### XXX: 'hextid': ('tid', ???),  ### decimal or hex integer (depending on APR version)
    },
    ### XXX: 't': (TIME_FIELD_TOKEN, ??? ),  ### strftime
    'T': {
        'ms': ('request_duration_milliseconds', PC.signed_integer),
        'us': ('request_duration_microseconds', PC.signed_integer),
        's': ('request_duration_seconds', PC.signed_integer),
    },
    '^ti': ('trailer_in', esc_string),
    '^to': ('trailer_out', esc_string),
}

directive = P.CharsNotIn("%")("literal") | P.Literal('%') + P.ZeroOrMore(
    P.Optional(P.Literal('!')) + P.delimitedList(PC.integer, ',')
    ^ (P.Literal("<") ^ P.Literal(">"))("redirect")
    ^ (P.Literal("{") + P.Optional(P.CharsNotIn("}"))("param") + P.Literal("}"))
) + (
    P.Literal("^") + P.Word(P.alphas, exact=2)
    ^ P.Word(P.alphas, exact=1)
)("directive")
directive.leaveWhitespace()

def format2parser(fmt, plain_directives=None, parameterized_directives=None):
    if plain_directives is None:
        plain_directives = PLAIN_DIRECTIVES
    if parameterized_directives is None:
        parameterized_directives = PARAMETERIZED_DIRECTIVES
    parser = P.Empty()
    ### TODO: Ensure that this processes the entire string (including, say,
    ### lone percent signs at the end of the string)
    for d in directive.searchString(fmt):
        if d.literal:
            parser += P.Literal(d.literal)
        else:
            try:
                if d.param:  # Apache treats an empty param the same as no param
                    spec = parameterized_directives[d.directive]
                    if isinstance(spec, dict):
                        name, p = spec[d.param]
                    #elif callable(spec):
                    else:
                        name = spec[0] + ':' + d.param
                        p = spec[1]
                else:
                    name, p = plain_directives[d.directive]
            except KeyError:
                raise InvalidDirectiveError(''.join(d))
            if name is None:
                parser += p
            else:
                if d.redirect == '<':
                    name = 'original_' + name
                elif d.redirect == '>':
                    name = 'final_' + name
                parser += p(name)
    parser.leaveWhitespace()
    print(repr(parser))
    return parser
