### cf. the log definitions shipped with Apache under Ubuntu (Debian?), which
### use %O instead of %b
COMMON_LOG_FORMAT = "%h %l %u %t \"%r\" %>s %b"
COMMON_LOG_VHOST_FORMAT = "%v %h %l %u %t \"%r\" %>s %b"
COMBINED_LOG_FORMAT = "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\""
REFERER_LOG_FORMAT = "%{Referer}i -> %U"
AGENT_LOG_FORMAT = "%{User-agent}i"
