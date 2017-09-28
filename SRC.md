- <http://httpd.apache.org/docs/current/mod/mod_log_config.html>
- Where various relevant things are defined in the Apache source:
    - `modules/loggers/mod_log_config.c`
        - table of format directive definitions: `log_pre_config()`
    - escaping of strings: `ap_escape_logitem()` in `server/util.c`
    - decisions on what to escape: uses of `T_ESCAPE_LOGITEM` in
      `server/gen_test_char.c`
    - definition of `request_rec`: `ap.d`
    - `log_pre_config()` in `modules/loggers/mod_logio.c`: `%I`, `%O`, `%S`,
      and `%^FB` formats
