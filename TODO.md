- Write tests
    - cf. <https://gist.github.com/rm-hull/bd60aed44024e9986e3c>?
- Expand README

- Research the following:
    - Look into whether the values for the following string format directives
      have more restrictive patterns they always follow:
        - `%C` - no semicolons, spaces, or tabs?  URI encoded?
        - `%H` — no restrictions? (at least on Trusty)
        - `%h`
        - `%f`?
        - `%l`
        - `%m`
        - `%q` - begins with `?` when non-empty
        - `%R`
        - `%u` - no colon?
        - `%v` - no whitespace?
        - `%V` - no whitespace?
        - `%{*}^ti`
        - `%{*}^to`
    - `mod_ssl` formats??? <http://httpd.apache.org/docs/current/mod/mod_ssl.html#logformats>
    - Can any format directive _not_ evaluate to `-`?
    - Check whether `%a` can be a comma-separated list of IP addresses (in case
      of proxying/X-Forwarded-For and the like)

- For each directive that doesn't match what one would naïvely expect, add a
  comment explaining why (including what versions of Apache the behavior is
  observed in)

- Test parsing entries that end in LF and/or CR LF

- For each format in `format.py` that Ubuntu (Debian?) ships using `%O` instead
  of `%b`, add a `%O`-using format with the name suffix `_UBUNTU` (`_DEBIAN`?)

- Include instructions in the documentation for adding your own format
  directives (including `%{*}t` sub-directives)

- Add a console script entry point: `apachelogs2json [--format <format>]
  [<file> ...]`
    - The special names "combined" and "common" (et alii?) are accepted as
      formats.
        - Accept these in the library interface as well?
    - Default format: combined?  Guess at combined or common?
