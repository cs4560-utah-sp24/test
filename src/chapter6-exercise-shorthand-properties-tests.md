Tests for WBE Chapter 6 Exercise `Shorthand Properties`
=======================

Description
-----------

CSS “shorthand properties” set multiple related CSS properties at the same time;
  for example, `font: italic bold 100% Times` sets the font-style, font-weight, 
  font-size, and font-family properties all at once. 
Add shorthand properties to your parser. 
(If you haven’t implemented font-family, just ignore that part.)

    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> import browser
    >>> def print_pairs(style):
    ...     for key in sorted(style):
    ...         val = style[key]
    ...         print(f"{key}: {val}")


There are many possible shorthand properties, but the only shorthand property we
  will be adding is the four property font variation.


    >>> pairs = browser.CSSParser("font: italic bold 100% Times;").body()
    >>> print_pairs(pairs)
    font-family: Times
    font-size: 100%
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

