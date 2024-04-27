Tests for WBE Chapter 3 Exercise `Superscripts`
==============================================

Add support for the `<sup>` tag. Text in this tag should be smaller
(perhaps half the normal text size) and be placed so that the top of a
superscript lines up with the top of a normal letter.

Tests
-----

Testing boilerplate:

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> _ = wbemocks.patch_canvas()
    >>> import browser
    >>> def test_layout(text):
    ...   dl = browser.Layout(browser.lex(text)).display_list
    ...   wbemocks.print_list(wbemocks.normalize_display_list(dl))

A superscript should have half the normal font size and be aligned to
the top of other text on the line.

    >>> test_layout("E=mc<sup>2</sup>")
    (13.0, 20.25, 'E=mc', Font size=12 weight=normal slant=roman style=None)
    (73.0, 20.25, '2', Font size=6 weight=normal slant=roman style=None)

Superscript text should be able to mix with normal text.

    >>> test_layout("B o <sup>o</sup> O <sup>O</sup>")
    (13.0, 20.25, 'B', Font size=12 weight=normal slant=roman style=None)
    (37.0, 20.25, 'o', Font size=12 weight=normal slant=roman style=None)
    (61.0, 20.25, 'o', Font size=6 weight=normal slant=roman style=None)
    (73.0, 20.25, 'O', Font size=12 weight=normal slant=roman style=None)
    (97.0, 20.25, 'O', Font size=6 weight=normal slant=roman style=None)

More than one word can be in a `<sup>` region.

    >>> test_layout("This <sup>is Sparta</sup>")
    (13.0, 20.25, 'This', Font size=12 weight=normal slant=roman style=None)
    (73.0, 20.25, 'is', Font size=6 weight=normal slant=roman style=None)
    (91.0, 20.25, 'Sparta', Font size=6 weight=normal slant=roman style=None)

The top alignment should be aligned to top even with large text on the line.

    >>> test_layout("<big>Big text</big> normal text <sup>super</sup>")
    (13.0, 21.0, 'Big', Font size=16 weight=normal slant=roman style=None)
    (77.0, 21.0, 'text', Font size=16 weight=normal slant=roman style=None)
    (157.0, 24.0, 'normal', Font size=12 weight=normal slant=roman style=None)
    (241.0, 24.0, 'text', Font size=12 weight=normal slant=roman style=None)
    (301.0, 21.0, 'super', Font size=6 weight=normal slant=roman style=None)
