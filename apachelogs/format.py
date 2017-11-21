### cf. the log definitions shipped with Apache under Ubuntu (Debian?), which
### use %O instead of %b
COMMON = "%h %l %u %t \"%r\" %>s %b"
COMMON_VHOST = "%v %h %l %u %t \"%r\" %>s %b"
COMBINED = "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\""
REFERER = "%{Referer}i -> %U"
AGENT = "%{User-agent}i"
