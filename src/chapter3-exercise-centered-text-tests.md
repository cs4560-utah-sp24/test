Tests for WBE Chapter 3 Exercise `Centered Text`
==============================================

Testing boilerplate:

    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> _ = test.patch_canvas()
    >>> import browser
    >>> def test_layout(text):
    ...   dl = browser.Layout(browser.lex(text)).display_list
    ...   return test.normalize_display_list(dl)

The headers mentioned in the exercise description are centered due to CSS, 
  which is the subject of chapter 6.
For now we will just center text inside any `h1 class="title"` tag.

    >>> browser.WIDTH = 800
    >>> test_layout('<h1 class="title">center me</h1>') #doctest: +NORMALIZE_WHITESPACE
    [(328.0, 21.0, 'center', Font size=16 weight=normal slant=roman style=None), 
     (440.0, 21.0, 'me', Font size=16 weight=normal slant=roman style=None)]

Encountering the opening `h1 class="title"`  should trigger a `flush`.

    >>> test_layout('first line<h1 class="title">center next line</h1>') #doctest: +NORMALIZE_WHITESPACE
    [(13.0, 21.0, 'first', Font size=16 weight=normal slant=roman style=None), 
     (109.0, 21.0, 'line', Font size=16 weight=normal slant=roman style=None), 
     (272.0, 41.0, 'center', Font size=16 weight=normal slant=roman style=None),
     (384.0, 41.0, 'next', Font size=16 weight=normal slant=roman style=None),
     (464.0, 41.0, 'line', Font size=16 weight=normal slant=roman style=None)]

Centering should be aware of the `WIDTH`.

    >>> browser.WIDTH = 200
    >>> test_layout('<h1 class="title">center me</h1>') #doctest: +NORMALIZE_WHITESPACE
    [(28.0, 21.0, 'center', Font size=16 weight=normal slant=roman style=None), 
     (140.0, 21.0, 'me', Font size=16 weight=normal slant=roman style=None)]

Centering should also be able to center different lines with different widths

    >>> browser.WIDTH = 800
    >>> test_layout('<h1 class="title">center me</h1><br><h1 class="title">also center me </h1>') #doctest: +NORMALIZE_WHITESPACE   
    [(328.0, 21.0, 'center', Font size=16 weight=normal slant=roman style=None), 
     (440.0, 21.0, 'me', Font size=16 weight=normal slant=roman style=None), 
     (288.0, 41.0, 'also', Font size=16 weight=normal slant=roman style=None), 
     (368.0, 41.0, 'center', Font size=16 weight=normal slant=roman style=None), 
     (480.0, 41.0, 'me', Font size=16 weight=normal slant=roman style=None)]

You should be able to mix centered and normal text on different lines

    >>> test_layout('<h1 class="title">center me</h1><br>do not center me<h1 class="title">but do center me</h1>') #doctest: +NORMALIZE_WHITESPACE   
    [(328.0, 21.0, 'center', Font size=16 weight=normal slant=roman style=None), 
     (440.0, 21.0, 'me', Font size=16 weight=normal slant=roman style=None), 
     (13.0, 41.0, 'do', Font size=16 weight=normal slant=roman style=None), 
     (61.0, 41.0, 'not', Font size=16 weight=normal slant=roman style=None),
     (125.0, 41.0, 'center', Font size=16 weight=normal slant=roman style=None),
     (237.0, 41.0, 'me', Font size=16 weight=normal slant=roman style=None), 
     (272.0, 61.0, 'but', Font size=16 weight=normal slant=roman style=None), 
     (336.0, 61.0, 'do', Font size=16 weight=normal slant=roman style=None), 
     (384.0, 61.0, 'center', Font size=16 weight=normal slant=roman style=None),
     (496.0, 61.0, 'me', Font size=16 weight=normal slant=roman style=None)]
