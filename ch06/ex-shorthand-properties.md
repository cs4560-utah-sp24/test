Tests for WBE Chapter 6 Exercise `Shorthand Properties`
=======================

CSS “shorthand properties” set multiple related CSS properties at the
same time; for example, `font: italic bold 100% Times` sets the
`font-style`, `font-weight`, `font-size`, and `font-family` properties
all at once. Add shorthand properties to your parser. (If you haven’t
implemented `font-family`, just ignore that part.)

Specifically, implement the `font` shorthand property, which should
expand into `font-style`, `font-weight`, `font-size`, and
`font-family`. Expand shorthand properties in the `body` function: it
should return the expanded properties but not the shorthand itself.

If the user provides fewer than 4 fields, use them in this order:

- If only one field is provided, only set `font-family`
- If two fields are provided, set `font-size` and `font-family`
- If three fields are provided, set `font-weight`, `font-size`, and
  `font-family`, unless the first field is "italic" in which case set
  `font-style` instead
- If more than four fields are provided, join the fourth onward with
  spaces to make up the `font-family`.

Tests
-----

We'll have a helper function to print CSS key-value pairs:

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> import browser
    >>> def print_pairs(style):
    ...     for key in sorted(style):
    ...         val = style[key]
    ...         print(f"{key}: {val}")

The `body` function should only have expanded properties:

    >>> pairs = browser.CSSParser("font: italic bold 100% Times;").body()
    >>> print_pairs(pairs)
    font-family: Times
    font-size: 100%
    font-style: italic
    font-weight: bold

Remember that property names are case-insensitive:

    >>> pairs = browser.CSSParser("FONT: italic bold 100% Times;").body()
    >>> print_pairs(pairs)
    font-family: Times
    font-size: 100%
    font-style: italic
    font-weight: bold
    
If fields are missing, don't expand into those:

    >>> print_pairs(browser.CSSParser("font: Times;").body())
    font-family: Times
    >>> print_pairs(browser.CSSParser("font: 120% Times;").body())
    font-family: Times
    font-size: 120%
    >>> print_pairs(browser.CSSParser("font: italic 120% Times;").body())
    font-family: Times
    font-size: 120%
    font-style: italic
    >>> print_pairs(browser.CSSParser("font: bold 120% Times;").body())
    font-family: Times
    font-size: 120%
    font-weight: bold
    >>> print_pairs(browser.CSSParser("font: italic bold 120% Times New Roman;").body())
    font-family: Times New Roman
    font-size: 120%
    font-style: italic
    font-weight: bold

There can also be other properties specified in the same body.

    >>> pairs = browser.CSSParser("font: normal normal 32px Menlo; color:yellow;").body()
    >>> print_pairs(pairs)
    color: yellow
    font-family: Menlo
    font-size: 32px
    font-style: normal
    font-weight: normal

    >>> pairs = browser.CSSParser("background: green; font: normal bold 90% Arial;").body()
    >>> print_pairs(pairs)
    background: green
    font-family: Arial
    font-size: 90%
    font-style: normal
    font-weight: bold

Later specifications override earlier ones.

    >>> pairs = browser.CSSParser("font: oblique normal 32px Kefa; font-size: 12px;").body()
    >>> print_pairs(pairs)
    font-family: Kefa
    font-size: 12px
    font-style: oblique
    font-weight: normal
    >>> pairs = browser.CSSParser("font-family: Optima; font: normal lighter 42px Skia;").body()
    >>> print_pairs(pairs)
    font-family: Skia
    font-size: 42px
    font-style: normal
    font-weight: lighter

Check if "font" is the last property in a rule body, with and without a final semicolon, ensuring correct parsing.

    >>> sel, pairs = browser.CSSParser("a { color: blue; font: bold 12px Arial; }").parse()[0]
    >>> print_pairs(pairs)
    color: blue
    font-family: Arial
    font-size: 12px
    font-weight: bold

    >>> sel, pairs = browser.CSSParser("a { color: blue; font: italic bold 14px Times New Roman }").parse()[0]
    >>> print_pairs(pairs)
    color: blue
    font-family: Times New Roman
    font-size: 14px
    font-style: italic
    font-weight: bold