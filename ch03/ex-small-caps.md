Tests for WBE Chapter 3 Exercise `Small Caps`
==============================================

Make the `<abbr>` element render text in small caps~~, like this~~.
Inside an `<abbr>` tag, lower-case letters should be small,
capitalized, and bold, while all other characters (upper case,
numbers, etc) should be drawn in the normal font.

Tests
-----

Testing boilerplate:

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> _ = wbemocks.patch_canvas()
    >>> import browser
    >>> browser.WIDTH
    800
    >>> def test_layout(text):
    ...   dl = browser.Layout(browser.lex(text)).display_list
    ...   wbemocks.print_list(wbemocks.normalize_display_list(dl))

For lowercase input use a bold font half the normal size, and convert all 
  characters to uppercase.

    >>> test_layout("<abbr>half</abbr>")
    (13.0, 19.125, 'HALF', Font size=6 weight=bold slant=roman style=None)

All characters that are not lowercase should use the normal font, and the 
  spacing between words should use the normal font as well.

    >>> test_layout("<abbr>1234 ABCD</abbr>")
    (13.0, 20.25, '1234', Font size=12 weight=normal slant=roman style=None)
    (73.0, 20.25, 'ABCD', Font size=12 weight=normal slant=roman style=None)

Combining the two we get small caps.
Runs of characters in a word that use the same font are presented using single 
  `display_list` entries.

    >>> test_layout("<abbr>Small Caps</abbr>")
    (13.0, 20.25, 'S', Font size=12 weight=normal slant=roman style=None)
    (25.0, 24.75, 'MALL', Font size=6 weight=bold slant=roman style=None)
    (61.0, 20.25, 'C', Font size=12 weight=normal slant=roman style=None)
    (73.0, 24.75, 'APS', Font size=6 weight=bold slant=roman style=None)

 Other text should not interfere with the small caps text.
 
    >>> test_layout("It's like YELLING <abbr>Quietly</abbr>")
    (13.0, 20.25, "It's", Font size=12 weight=normal slant=roman style=None)
    (73.0, 20.25, 'like', Font size=12 weight=normal slant=roman style=None)
    (133.0, 20.25, 'YELLING', Font size=12 weight=normal slant=roman style=None)
    (229.0, 20.25, 'Q', Font size=12 weight=normal slant=roman style=None)
    (241.0, 24.75, 'UIETLY', Font size=6 weight=bold slant=roman style=None)

    >>> test_layout("<big><abbr>example</abbr></big>")
    (13.0, 19.5, 'EXAMPLE', Font size=8 weight=bold slant=roman style=None)

    >>> test_layout("<abbr>small<big>example</big>text</abbr>")
    (13.0, 21.0, 'SMALL', Font size=6 weight=bold slant=roman style=None)
    (55.0, 19.5, 'EXAMPLE', Font size=8 weight=bold slant=roman style=None)
    (127.0, 21.0, 'TEXT', Font size=6 weight=bold slant=roman style=None)

    >>> test_layout("<abbr>multi<br>line<br>text</abbr>")
    (13.0, 19.125, 'MULTI', Font size=6 weight=bold slant=roman style=None)
    (13.0, 26.625, 'LINE', Font size=6 weight=bold slant=roman style=None)
    (13.0, 34.125, 'TEXT', Font size=6 weight=bold slant=roman style=None)

    >>> test_layout("<abbr>LoTs Of CaSe ChAnGeS</abbr>")
    (13.0, 20.25, 'L', Font size=12 weight=normal slant=roman style=None)
    (25.0, 24.75, 'O', Font size=6 weight=bold slant=roman style=None)
    (31.0, 20.25, 'T', Font size=12 weight=normal slant=roman style=None)
    (43.0, 24.75, 'S', Font size=6 weight=bold slant=roman style=None)
    (61.0, 20.25, 'O', Font size=12 weight=normal slant=roman style=None)
    (73.0, 24.75, 'F', Font size=6 weight=bold slant=roman style=None)
    (91.0, 20.25, 'C', Font size=12 weight=normal slant=roman style=None)
    (103.0, 24.75, 'A', Font size=6 weight=bold slant=roman style=None)
    (109.0, 20.25, 'S', Font size=12 weight=normal slant=roman style=None)
    (121.0, 24.75, 'E', Font size=6 weight=bold slant=roman style=None)
    (139.0, 20.25, 'C', Font size=12 weight=normal slant=roman style=None)
    (151.0, 24.75, 'H', Font size=6 weight=bold slant=roman style=None)
    (157.0, 20.25, 'A', Font size=12 weight=normal slant=roman style=None)
    (169.0, 24.75, 'N', Font size=6 weight=bold slant=roman style=None)
    (175.0, 20.25, 'G', Font size=12 weight=normal slant=roman style=None)
    (187.0, 24.75, 'E', Font size=6 weight=bold slant=roman style=None)
    (193.0, 20.25, 'S', Font size=12 weight=normal slant=roman style=None)
