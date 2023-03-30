Tests for WBE Chapter 3
=======================

Chapter 3 (Formatting Text) adds on font metrics and simple font styling via
HTML tags. This file contains tests for the additional functionality.

    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
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

    >>> def test_layout(text):
    ...   dl = browser.Layout(browser.lex(text)).display_list
    ...   return test.normalize_display_list(dl)

    >>> test_layout("abc")
    [(13.0, 21.0, 'abc', Font size=16 weight=normal slant=roman style=None)]

    >>> test_layout("<b>abc</b>")
    [(13.0, 21.0, 'abc', Font size=16 weight=bold slant=roman style=None)]
    
    >>> test_layout("<big>abc</big>")
    [(13.0, 21.75, 'abc', Font size=20 weight=normal slant=roman style=None)]

    >>> test_layout("<big><big>abc</big></big>")
    [(13.0, 22.5, 'abc', Font size=24 weight=normal slant=roman style=None)]

    >>> test_layout("<big><big><i>abc</i></big></big>")
    [(13.0, 22.5, 'abc', Font size=24 weight=normal slant=italic style=None)]

    >>> test_layout("<big><big><i>abc</i></big>def</big>") #doctest: +NORMALIZE_WHITESPACE
    [(13.0, 22.5, 'abc', Font size=24 weight=normal slant=italic style=None), 
     (109.0, 25.5, 'def', Font size=20 weight=normal slant=roman style=None)]

Lines of text are spaced to make room for the tallest text. Let's lay
out text with mixed font sizes, and then measure the line heights:

    >>> def baseline(word):
    ...     return word[1] + word[3].metrics("ascent")

    >>> test_layout("Start<br>Regular<br>Regular <big><big>Big") #doctest: +NORMALIZE_WHITESPACE 
    [(13.0, 21.0, 'Start', Font size=16 weight=normal slant=roman style=None), 
     (13.0, 41.0, 'Regular', Font size=16 weight=normal slant=roman style=None),
     (13.0, 68.5, 'Regular', Font size=16 weight=normal slant=roman style=None), 
     (141.0, 62.5, 'Big', Font size=24 weight=normal slant=roman style=None)]

    >>> display_list = test_layout("Start<br>Regular<br>Regular <big><big>Big")
    >>> baseline(display_list[1]) - baseline(display_list[0])
    20.0
    >>> baseline(display_list[3]) - baseline(display_list[1])
    27.5

The differing line heights don't occur when text gets smaller:


    >>> test_layout("Start<br>Regular<br>Regular <small><small>Small")  #doctest: +NORMALIZE_WHITESPACE 
    [(13.0, 21.0, 'Start', Font size=16 weight=normal slant=roman style=None),
     (13.0, 41.0, 'Regular', Font size=16 weight=normal slant=roman style=None),
     (13.0, 61.0, 'Regular', Font size=16 weight=normal slant=roman style=None), 
     (141.0, 64.0, 'Small', Font size=12 weight=normal slant=roman style=None)]

    >>> display_list = test_layout("Start<br>Regular<br>Regular <small><small>Small")
    >>> baseline(display_list[1]) - baseline(display_list[0])
    20.0
    >>> baseline(display_list[3]) - baseline(display_list[1])
    20.0


Testing `Browser`
-----------------

Now let's test integration of layout into the Browser class.

    >>> url = 'http://test.test/chapter3-example1'
    >>> test.socket.respond_200(url=url, 
    ...   body="<small>abc<i>def</i></small>")
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)

Testing the display list output of this URL:

    >>> test.normalize_display_list(this_browser.display_list)  #doctest: +NORMALIZE_WHITESPACE 
    [(13.0, 20.625, 'abc', Font size=14 weight=normal slant=roman style=None), 
     (69.0, 20.625, 'def', Font size=14 weight=normal slant=italic style=None)]

And the canvas:

    >>> test.patch_canvas()
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    create_text: x=13 y=20.625 text=abc font=Font size=14 weight=normal slant=roman style=None anchor=nw
    create_text: x=69 y=20.625 text=def font=Font size=14 weight=normal slant=italic style=None anchor=nw
    >>> test.unpatch_canvas()
