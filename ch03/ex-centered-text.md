Tests for WBE Chapter 3 Exercise `Centered Text`
==============================================

This book’s page titles are centered; make your browser do the same
for text between `<h1 class="title">` and `</h1>`. Each line has to be
centered individually, because different lines will have different
lengths.

Tests
-----

Testing boilerplate:

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> _ = wbemocks.patch_canvas()
    >>> import browser

The headers mentioned in the exercise description are centered due to
CSS, which is the subject of chapter 6. In this exercise, we will just
treat `h1 class="title"` as a special centering tag. Among other
things, both the open and close tags should flush lines, because it
doesn't make sense to have a line where half the line is centered and
the other half isn't.

Let's define some testing shortcuts:

    >>> browser.WIDTH
    800
    >>> def test_layout(text):
    ...   dl = browser.Layout(browser.lex(text)).display_list
    ...   wbemocks.print_list(wbemocks.normalize_display_list(dl))

Centering a line of text works:

    >>> test_layout('<h1 class="title">center me</h1>')
    (328.0, 21.0, 'center', Font size=16 weight=normal slant=roman style=None)
    (440.0, 21.0, 'me', Font size=16 weight=normal slant=roman style=None)

Encountering the opening `h1 class="title"`  should trigger a `flush`.

    >>> test_layout('first line<h1 class="title">center next line</h1>')
    (13.0, 21.0, 'first', Font size=16 weight=normal slant=roman style=None)
    (109.0, 21.0, 'line', Font size=16 weight=normal slant=roman style=None)
    (272.0, 41.0, 'center', Font size=16 weight=normal slant=roman style=None)
    (384.0, 41.0, 'next', Font size=16 weight=normal slant=roman style=None)
    (464.0, 41.0, 'line', Font size=16 weight=normal slant=roman style=None)

Centering should be aware of the `WIDTH`.

    >>> browser.set_parameters(WIDTH=200)
    >>> test_layout('<h1 class="title">center me</h1>')
    (28.0, 21.0, 'center', Font size=16 weight=normal slant=roman style=None)
    (140.0, 21.0, 'me', Font size=16 weight=normal slant=roman style=None)

Centering should also be able to center different lines with different widths

    >>> browser.set_parameters(WIDTH=800)
    >>> test_layout('<h1 class="title">center me</h1><br><h1 class="title">also center me </h1>')
    (328.0, 21.0, 'center', Font size=16 weight=normal slant=roman style=None)
    (440.0, 21.0, 'me', Font size=16 weight=normal slant=roman style=None)
    (288.0, 41.0, 'also', Font size=16 weight=normal slant=roman style=None)
    (368.0, 41.0, 'center', Font size=16 weight=normal slant=roman style=None)
    (480.0, 41.0, 'me', Font size=16 weight=normal slant=roman style=None)

You should be able to mix centered and normal text on different lines

    >>> test_layout('<h1 class="title">center me</h1><br>do not center me<h1 class="title">but do center me</h1>')
    (328.0, 21.0, 'center', Font size=16 weight=normal slant=roman style=None)
    (440.0, 21.0, 'me', Font size=16 weight=normal slant=roman style=None)
    (13.0, 41.0, 'do', Font size=16 weight=normal slant=roman style=None)
    (61.0, 41.0, 'not', Font size=16 weight=normal slant=roman style=None)
    (125.0, 41.0, 'center', Font size=16 weight=normal slant=roman style=None)
    (237.0, 41.0, 'me', Font size=16 weight=normal slant=roman style=None)
    (272.0, 61.0, 'but', Font size=16 weight=normal slant=roman style=None)
    (336.0, 61.0, 'do', Font size=16 weight=normal slant=roman style=None)
    (384.0, 61.0, 'center', Font size=16 weight=normal slant=roman style=None)
    (496.0, 61.0, 'me', Font size=16 weight=normal slant=roman style=None)


Ensure that the application correctly handles the transition from centered to regular text within the same sequence

    >>> test_layout('<h1 class="title">center this</h1>then this is regular')
    (312.0, 21.0, 'center', Font size=16 weight=normal slant=roman style=None)
    (424.0, 21.0, 'this', Font size=16 weight=normal slant=roman style=None)
    (13.0, 41.0, 'then', Font size=16 weight=normal slant=roman style=None)
    (93.0, 41.0, 'this', Font size=16 weight=normal slant=roman style=None)
    (173.0, 41.0, 'is', Font size=16 weight=normal slant=roman style=None)
    (221.0, 41.0, 'regular', Font size=16 weight=normal slant=roman style=None)
