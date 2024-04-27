Tests for WBE Chapter 3
=======================

Chapter 3 (Formatting Text) adds on font metrics and simple font styling via
HTML tags. This file contains tests for the additional functionality.

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> import browser

Make sure you have the expected default values for `HSTEP`, `VSTEP`,
`WIDTH`, and `HEIGHT`.

    >>> browser.HSTEP
    13
    >>> browser.VSTEP
    18
    >>> browser.WIDTH
    800
    >>> browser.HEIGHT
    600

Testing `lex`
-------------

The `lex` function in chapter three has been beefed up to return an array
of `Tag` or `Text` objects, rather than just the stream of characters from the
input.

To allow us to print these in a readable form please add a `__repr__(self):` method
  to your `Tag` and `Text` classes.
The bodies of these methods should, respectively, be
`return "Tag('{}')".format(self.tag)`
and `return "Text('{}')".format(self.text)`

    >>> browser.lex('<body>hello</body>')
    [Tag('body'), Text('hello'), Tag('/body')]
    >>> browser.lex('he<body>llo</body>')
    [Text('he'), Tag('body'), Text('llo'), Tag('/body')]
    >>> browser.lex('he<body>l</body>lo')
    [Text('he'), Tag('body'), Text('l'), Tag('/body'), Text('lo')]
    >>> browser.lex('he<body>l<div>l</div>o</body>')
    [Text('he'), Tag('body'), Text('l'), Tag('div'), Text('l'), Tag('/div'), Text('o'), Tag('/body')]
    >>> browser.lex('hello world')
    [Text('hello world')]


Note that the tags do not have to match:

    >>> browser.lex('he<body>l</div>lo')
    [Text('he'), Tag('body'), Text('l'), Tag('/div'), Text('lo')]
    >>> browser.lex('he<body>l<div>l</body>o</div>')
    [Text('he'), Tag('body'), Text('l'), Tag('div'), Text('l'), Tag('/body'), Text('o'), Tag('/div')]

Testing `Layout`
----------------

This chapter also creates a Layout class to output a display list that can
format text. However, note that this test doesn't use real tkinter fonts, but
rather a mock font that has faked metrics.

    >>> def make_layout(text):
    ...   dl = browser.Layout(browser.lex(text)).display_list
    ...   return wbemocks.normalize_display_list(dl)
    >>> def test_layout(text):
    ...   wbemocks.print_list(make_layout(text))

    >>> test_layout("abc")
    (13.0, 20.25, 'abc', Font size=12 weight=normal slant=roman style=None)

    >>> test_layout("<b>abc</b>")
    (13.0, 20.25, 'abc', Font size=12 weight=bold slant=roman style=None)
    
    >>> test_layout("<big>abc</big>")
    (13.0, 21.0, 'abc', Font size=16 weight=normal slant=roman style=None)

    >>> test_layout("<big><big>abc</big></big>")
    (13.0, 21.75, 'abc', Font size=20 weight=normal slant=roman style=None)

    >>> test_layout("<big><big><i>abc</i></big></big>")
    (13.0, 21.75, 'abc', Font size=20 weight=normal slant=italic style=None)

    >>> test_layout("<big><big><i>abc</i></big>def</big>")
    (13.0, 21.75, 'abc', Font size=20 weight=normal slant=italic style=None)
    (93.0, 24.75, 'def', Font size=16 weight=normal slant=roman style=None)

Lines of text are spaced to make room for the tallest text. Let's lay
out text with mixed font sizes, and then measure the line heights:

    >>> def baseline(word):
    ...     return word[1] + word[3].metrics("ascent")

    >>> test_layout("Start<br>Regular<br>Regular <big><big>Big")
    (13.0, 20.25, 'Start', Font size=12 weight=normal slant=roman style=None)
    (13.0, 35.25, 'Regular', Font size=12 weight=normal slant=roman style=None)
    (13.0, 57.75, 'Regular', Font size=12 weight=normal slant=roman style=None)
    (109.0, 51.75, 'Big', Font size=20 weight=normal slant=roman style=None)

    >>> display_list = make_layout("Start<br>Regular<br>Regular <big><big>Big")
    >>> baseline(display_list[1]) - baseline(display_list[0])
    15.0
    >>> baseline(display_list[3]) - baseline(display_list[1])
    22.5

The differing line heights don't occur when text gets smaller:


    >>> test_layout("Start<br>Regular<br>Regular <small><small>Small")
    (13.0, 20.25, 'Start', Font size=12 weight=normal slant=roman style=None)
    (13.0, 35.25, 'Regular', Font size=12 weight=normal slant=roman style=None)
    (13.0, 50.25, 'Regular', Font size=12 weight=normal slant=roman style=None)
    (109.0, 53.25, 'Small', Font size=8 weight=normal slant=roman style=None)

    >>> display_list = make_layout("Start<br>Regular<br>Regular <small><small>Small")
    >>> baseline(display_list[1]) - baseline(display_list[0])
    15.0
    >>> baseline(display_list[3]) - baseline(display_list[1])
    15.0


Testing `Browser`
-----------------

Now let's test integration of layout into the Browser class.

    >>> url = wbemocks.socket.serve("<small>abc<i>def</i></small>")
    >>> this_browser = browser.Browser()
    >>> this_browser.load(browser.URL(url))

Testing the display list output of this URL:

    >>> dl = wbemocks.normalize_display_list(this_browser.display_list)
    >>> wbemocks.print_list(dl)
    (13.0, 19.875, 'abc', Font size=10 weight=normal slant=roman style=None)
    (53.0, 19.875, 'def', Font size=10 weight=normal slant=italic style=None)

And the canvas:

    >>> wbemocks.patch_canvas()
    >>> this_browser = browser.Browser()
    >>> this_browser.load(browser.URL(url))
    create_text: x=13 y=19.875 text=abc font=Font size=10 weight=normal slant=roman style=None anchor=nw
    create_text: x=53 y=19.875 text=def font=Font size=10 weight=normal slant=italic style=None anchor=nw
    >>> wbemocks.unpatch_canvas()


Test with multiple words (do not forget to split on word)

    >>> content = "hello world"
    >>> url = browser.URL(wbemocks.socket.serve(content))
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    >>> def test_layout(content):
    ...   dl = browser.Layout(browser.lex(content)).display_list
    ...   wbemocks.print_list(wbemocks.normalize_display_list(dl))
    >>> test_layout(content)
    (13.0, 20.25, 'hello', Font size=12 weight=normal slant=roman style=None)
    (85.0, 20.25, 'world', Font size=12 weight=normal slant=roman style=None)
