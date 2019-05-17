- Research the following:
    - Look into whether the values for the following string format directives
      have more restrictive patterns they always follow:
        - `%h`
        - `%m` - no whitespace?
        - `%q` - no whitespace? no '#'?
        - `%v` - no whitespace?
        - `%V` - no whitespace?
        - `%{*}^ti`
        - `%{*}^to`
    - Check whether `%a` can be a comma-separated list of IP addresses (in case
      of proxying/X-Forwarded-For and the like)

- Test every directive

- For each directive that doesn't match what one would naïvely expect, add a
  comment explaining why (including what versions of Apache the behavior is
  observed in)

- Include instructions in the documentation for adding your own format
  directives (including `%{*}t` sub-directives)

- Add a console script entry point: `apachelogs2json [--format <format>]
  [<file> ...]`
    - The special names "combined" and "common" (et alii?) are accepted as
      formats.
        - Accept these in the library interface as well?
    - Default format: combined?  Guess at combined or common?
