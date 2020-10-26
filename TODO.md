- Research the following:
    - Is it valid to expect `%h`, `%v`, and `%V` to always be hostnames (or an
      IP address, for `%h`)?  Failing that, can they at least be expected to
      not contain whitespace?
    - Check whether `%a` can be a comma-separated list of IP addresses (in case
      of proxying/X-Forwarded-For and the like)

- Test every directive

- For each directive that doesn't match what one would naïvely expect, add a
  comment explaining why (including what versions of Apache the behavior is
  observed in)

- Include instructions in the documentation for adding your own format
  directives (including `%{*}t` sub-directives)
    - Instead of having users modify stuff directly, provide functions like
      `register_plain_directive(directive, name, pattern, converter)`
        - Add a `DirectiveRegistry` class with methods for registering new
          directives so that we aren't modifying the global state?
            - Make the LogParser constructor "private" and have instances
              instead be constructed through a method of DirectiveRegistry,
              with a global function version provided that uses a private
              registry of default values only?
                - Alternatively, give the LogParser constructor a
                  `registry=None` argument that defaults to the private default
                  registry?
            - Give the DirectiveRegistry class `parse()` and `parse_lines()`
              methods, with the global functions operating on a private
              registry of default values only

- Add a console script entry point: `apachelogs2json [--format <format>]
  [<file> ...]`
    - The special names "combined" and "common" (et alii?) are accepted as
      formats.
    - Default format: combined?  Guess at combined or common?
