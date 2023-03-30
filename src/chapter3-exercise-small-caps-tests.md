Tests for WBE Chapter 3 Exercise `Small Caps`
==============================================

Testing boilerplate:

    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> _ = test.patch_canvas()
    >>> import browser
    >>> browser.WIDTH = 800
    >>> def test_layout(text):
    ...   dl = browser.Layout(browser.lex(text)).display_list
    ...   return test.normalize_display_list(dl)

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
