Tests for WBE Chapter 3 Exercise `Soft Hyphens`
==============================================

Testing boilerplate:

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> _ = wbemocks.patch_canvas()
    >>> import browser
    >>> def test_layout(text):
    ...   dl = browser.Layout(browser.lex(text)).display_list
    ...   return wbemocks.normalize_display_list(dl)

Soft hyphens allow text to hint at where breaks can be inserted. If a
word is too wide to fit on the current line and contains a soft hyphen
it can be split and a literal hyphen placed at the break. For any
given word, only one display list item should be generated per line.

    >>> browser.set_parameters(WIDTH=128)
    >>> test_layout("Hello\N{soft hyphen}World") #doctest: +NORMALIZE_WHITESPACE
    [(13.0, 21.0, 'Hello-', Font size=16 weight=normal slant=roman style=None),
     (13.0, 41.0, 'World', Font size=16 weight=normal slant=roman style=None)]

If the word fits without splitting then no literal hyphens are present.

    >>> browser.set_parameters(WIDTH=800)
    >>> test_layout("Hello\N{soft hyphen}World")
    [(13.0, 21.0, 'HelloWorld', Font size=16 weight=normal slant=roman style=None)]

When a soft hyphen is replaced with a literal hyphen you need to check that the
  text with the hyphen fits on the line.

    >>> browser.set_parameters(WIDTH=90)
    >>> test_layout("a\N{soft hyphen}b\N{soft hyphen}c\N{soft hyphen}d\N{soft hyphen}e") #doctest: +NORMALIZE_WHITESPACE
    [(13.0, 21.0, 'abc-', Font size=16 weight=normal slant=roman style=None), 
     (13.0, 41.0, 'de', Font size=16 weight=normal slant=roman style=None)]


Sometimes a word may be so long that it needs to be split multiple times.

    >>> browser.set_parameters(WIDTH=122)
    >>> test_layout("multi\N{soft hyphen}word\N{soft hyphen}split") #doctest: +NORMALIZE_WHITESPACE
    [(13.0, 21.0, 'multi-', Font size=16 weight=normal slant=roman style=None), 
     (13.0, 41.0, 'word-', Font size=16 weight=normal slant=roman style=None),
     (13.0, 61.0, 'split', Font size=16 weight=normal slant=roman style=None)]
     
    >>> test_layout("multi\N{soft hyphen}word\N{soft hyphen}split\N{soft hyphen}four") #doctest: +NORMALIZE_WHITESPACE
    [(13.0, 21.0, 'multi-', Font size=16 weight=normal slant=roman style=None), 
     (13.0, 41.0, 'word-', Font size=16 weight=normal slant=roman style=None),
     (13.0, 61.0, 'splitfour', Font size=16 weight=normal slant=roman style=None)]
