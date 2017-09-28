- Research the following:
    - Look into whether the values for the following string format directives
      have more restrictive patterns they always follow:
        - `%H` — no restrictions? (at least on Trusty)
        - `%h`
        - `%f`?
        - `%l`
        - `%m`
        - `%q`
        - `%R`
        - `%u` (No colon?)
        - `%v`
        - `%V`
        - `%{*}^ti`
        - `%{*}^to`
    - `mod_ssl` formats??? <http://httpd.apache.org/docs/current/mod/mod_ssl.html#logformats>
    - Can any format directive _not_ evaluate to `-`?
    - Nginx logfile formats

- Handle format directives that filter by status code
- Handle `<` and `>` modifiers for internally-redirected requests
- Change the human names of format directives to match the names used in the
  Apache source
