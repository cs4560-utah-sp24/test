Tests for WBE Chapter 3 Exercise `Small Caps`
==============================================

Testing boilerplate:

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> _ = wbemocks.patch_canvas()
    >>> import browser
    >>> browser.WIDTH = 800
    >>> def test_layout(text):
    ...   dl = browser.Layout(browser.lex(text)).display_list
    ...   return wbemocks.normalize_display_list(dl)

For lowercase input use a bold font half the normal size, and convert all 
  characters to uppercase.

    >>> test_layout("<abbr>half</abbr>") #doctest: +NORMALIZE_WHITESPACE
    [(13.0, 19.5, 'HALF', Font size=8 weight=bold slant=roman style=None)]

All characters that are not lowercase should use the normal font, and the 
  spacing between words should use the normal font as well.

    >>> test_layout("<abbr>1234 ABCD</abbr>") #doctest: +NORMALIZE_WHITESPACE
    [(13.0, 21.0, '1234', Font size=16 weight=normal slant=roman style=None),
     (93.0, 21.0, 'ABCD', Font size=16 weight=normal slant=roman style=None)]

Combining the two we get small caps.
Runs of characters in a word that use the same font are presented using single 
  `display_list` entries.

    >>> test_layout("<abbr>Small Caps</abbr>") #doctest: +NORMALIZE_WHITESPACE
    [(13.0, 21.0, 'S', Font size=16 weight=normal slant=roman style=None), 
     (29.0, 27.0, 'MALL', Font size=8 weight=bold slant=roman style=None), 
     (77.0, 21.0, 'C', Font size=16 weight=normal slant=roman style=None), 
     (93.0, 27.0, 'APS', Font size=8 weight=bold slant=roman style=None)]

 Other text should not interfere with the small caps text.
 
    >>> test_layout("It's like YELLING <abbr>Quietly</abbr>") #doctest: +NORMALIZE_WHITESPACE
    [(13.0, 21.0, "It's", Font size=16 weight=normal slant=roman style=None), 
     (93.0, 21.0, 'like', Font size=16 weight=normal slant=roman style=None),
     (173.0, 21.0, 'YELLING', Font size=16 weight=normal slant=roman style=None),
     (301.0, 21.0, 'Q', Font size=16 weight=normal slant=roman style=None), 
     (317.0, 27.0, 'UIETLY', Font size=8 weight=bold slant=roman style=None)]

    >>> test_layout("<big><abbr>example</abbr></big>") #doctest: +NORMALIZE_WHITESPACE
    [(13.0, 19.875, 'EXAMPLE', Font size=10 weight=bold slant=roman style=None)]

    >>> test_layout("<abbr>small<big>example</big>text</abbr>") #doctest: +NORMALIZE_WHITESPACE
    [(13.0, 21.375, 'SMALL', Font size=8 weight=bold slant=roman style=None), 
    (69.0, 19.875, 'EXAMPLE', Font size=10 weight=bold slant=roman style=None), 
    (159.0, 21.375, 'TEXT', Font size=8 weight=bold slant=roman style=None)]

    >>> test_layout("<abbr>multi<br>line<br>text</abbr>") #doctest: +NORMALIZE_WHITESPACE
    [(13.0, 19.5, 'MULTI', Font size=8 weight=bold slant=roman style=None),
    (13.0, 29.5, 'LINE', Font size=8 weight=bold slant=roman style=None),
    (13.0, 39.5, 'TEXT', Font size=8 weight=bold slant=roman style=None)]

    >>> test_layout("<abbr>LoTs Of CaSe ChAnGeS</abbr>") #doctest: +NORMALIZE_WHITESPACE
    [(13.0, 21.0, 'L', Font size=16 weight=normal slant=roman style=None), 
    (29.0, 27.0, 'O', Font size=8 weight=bold slant=roman style=None), 
    (37.0, 21.0, 'T', Font size=16 weight=normal slant=roman style=None), 
    (53.0, 27.0, 'S', Font size=8 weight=bold slant=roman style=None), 
    (77.0, 21.0, 'O', Font size=16 weight=normal slant=roman style=None), 
    (93.0, 27.0, 'F', Font size=8 weight=bold slant=roman style=None), 
    (117.0, 21.0, 'C', Font size=16 weight=normal slant=roman style=None), 
    (133.0, 27.0, 'A', Font size=8 weight=bold slant=roman style=None), 
    (141.0, 21.0, 'S', Font size=16 weight=normal slant=roman style=None), 
    (157.0, 27.0, 'E', Font size=8 weight=bold slant=roman style=None), 
    (181.0, 21.0, 'C', Font size=16 weight=normal slant=roman style=None), 
    (197.0, 27.0, 'H', Font size=8 weight=bold slant=roman style=None), 
    (205.0, 21.0, 'A', Font size=16 weight=normal slant=roman style=None), 
    (221.0, 27.0, 'N', Font size=8 weight=bold slant=roman style=None),
    (229.0, 21.0, 'G', Font size=16 weight=normal slant=roman style=None),
    (245.0, 27.0, 'E', Font size=8 weight=bold slant=roman style=None), 
    (253.0, 21.0, 'S', Font size=16 weight=normal slant=roman style=None)]
