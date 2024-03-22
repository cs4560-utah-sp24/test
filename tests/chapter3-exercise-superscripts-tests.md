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
    ...   return wbemocks.normalize_display_list(dl)

A superscript should have half the normal font size and be aligned to
the top of other text on the line.

    >>> test_layout("E=mc<sup>2</sup>") #doctest: +NORMALIZE_WHITESPACE
    [(13.0, 21.0, 'E=mc', Font size=16 weight=normal slant=roman style=None),
     (93.0, 21.0, '2', Font size=8 weight=normal slant=roman style=None)]

Superscript text should be able to mix with normal text.

    >>> test_layout("B o <sup>o</sup> O <sup>O</sup>") #doctest: +NORMALIZE_WHITESPACE
    [(13.0, 21.0, 'B', Font size=16 weight=normal slant=roman style=None), 
     (45.0, 21.0, 'o', Font size=16 weight=normal slant=roman style=None), 
     (77.0, 21.0, 'o', Font size=8 weight=normal slant=roman style=None), 
     (93.0, 21.0, 'O', Font size=16 weight=normal slant=roman style=None), 
     (125.0, 21.0, 'O', Font size=8 weight=normal slant=roman style=None)]

More than one word can be in a `<sup>` region.

    >>> test_layout("This <sup>is Sparta</sup>") #doctest: +NORMALIZE_WHITESPACE
    [(13.0, 21.0, 'This', Font size=16 weight=normal slant=roman style=None),
     (93.0, 21.0, 'is', Font size=8 weight=normal slant=roman style=None),
     (117.0, 21.0, 'Sparta', Font size=8 weight=normal slant=roman style=None)]

The top alignment should be aligned to top even with large text on the line.

    >>> test_layout("<big>Big text</big> normal text <sup>super</sup>") #doctest: +NORMALIZE_WHITESPACE
    [(13.0, 21.75, 'Big', Font size=20 weight=normal slant=roman style=None),
     (93.0, 21.75, 'text', Font size=20 weight=normal slant=roman style=None),
     (193.0, 24.75, 'normal', Font size=16 weight=normal slant=roman style=None),
     (305.0, 24.75, 'text', Font size=16 weight=normal slant=roman style=None), 
     (385.0, 21.75, 'super', Font size=8 weight=normal slant=roman style=None)]
