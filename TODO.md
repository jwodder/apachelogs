- Write tests
    - cf. <https://gist.github.com/rm-hull/bd60aed44024e9986e3c>?
- Fill in keywords & classifiers
- Write README
- Rename to `accesslogs`?

- Research the following:
    - Look into whether the values for the following string format directives
      have more restrictive patterns they always follow:
        - `%C` - no semicolons, spaces, or tabs?  URI encoded?
        - `%H` — no restrictions? (at least on Trusty)
        - `%h`
        - `%f`?
        - `%l`
        - `%m`
        - `%q`
        - `%R`
        - `%u` - no colon?
        - `%v` - no whitespace?
        - `%V` - no whitespace?
        - `%{*}^ti`
        - `%{*}^to`
    - `mod_ssl` formats??? <http://httpd.apache.org/docs/current/mod/mod_ssl.html#logformats>
    - Can any format directive _not_ evaluate to `-`?
    - Nginx logfile formats

- Handle format directives that filter by status code
    - Should they be represented in the result dict/object differently than
      non-filtered directives?
- Handle `<` and `>` modifiers for internally-redirected requests
- Handle bytes input
    - What encoding are Apache logs written in?  Always ASCII?
