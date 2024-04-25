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
    (346.0, 20.25, 'center', Font size=12 weight=normal slant=roman style=None)
    (430.0, 20.25, 'me', Font size=12 weight=normal slant=roman style=None)

Encountering the opening `h1 class="title"`  should trigger a `flush`.

    >>> test_layout('first line<h1 class="title">center next line</h1>')
    (13.0, 20.25, 'first', Font size=12 weight=normal slant=roman style=None)
    (85.0, 20.25, 'line', Font size=12 weight=normal slant=roman style=None)
    (304.0, 35.25, 'center', Font size=12 weight=normal slant=roman style=None)
    (388.0, 35.25, 'next', Font size=12 weight=normal slant=roman style=None)
    (448.0, 35.25, 'line', Font size=12 weight=normal slant=roman style=None)

Centering should be aware of the `WIDTH`.

    >>> browser.set_parameters(WIDTH=200)
    >>> test_layout('<h1 class="title">center me</h1>')
    (46.0, 20.25, 'center', Font size=12 weight=normal slant=roman style=None)
    (130.0, 20.25, 'me', Font size=12 weight=normal slant=roman style=None)

Centering should also be able to center different lines with different widths

    >>> browser.set_parameters(WIDTH=800)
    >>> test_layout('<h1 class="title">center me</h1><br><h1 class="title">also center me </h1>')
    (346.0, 20.25, 'center', Font size=12 weight=normal slant=roman style=None)
    (430.0, 20.25, 'me', Font size=12 weight=normal slant=roman style=None)
    (316.0, 35.25, 'also', Font size=12 weight=normal slant=roman style=None)
    (376.0, 35.25, 'center', Font size=12 weight=normal slant=roman style=None)
    (460.0, 35.25, 'me', Font size=12 weight=normal slant=roman style=None)

You should be able to mix centered and normal text on different lines

    >>> test_layout('<h1 class="title">center me</h1><br>do not center me<h1 class="title">but do center me</h1>')
    (346.0, 20.25, 'center', Font size=12 weight=normal slant=roman style=None)
    (430.0, 20.25, 'me', Font size=12 weight=normal slant=roman style=None)
    (13.0, 35.25, 'do', Font size=12 weight=normal slant=roman style=None)
    (49.0, 35.25, 'not', Font size=12 weight=normal slant=roman style=None)
    (97.0, 35.25, 'center', Font size=12 weight=normal slant=roman style=None)
    (181.0, 35.25, 'me', Font size=12 weight=normal slant=roman style=None)
    (304.0, 50.25, 'but', Font size=12 weight=normal slant=roman style=None)
    (352.0, 50.25, 'do', Font size=12 weight=normal slant=roman style=None)
    (388.0, 50.25, 'center', Font size=12 weight=normal slant=roman style=None)
    (472.0, 50.25, 'me', Font size=12 weight=normal slant=roman style=None)


Ensure that the application correctly handles the transition from centered to regular text within the same sequence

    >>> test_layout('<h1 class="title">center this</h1>then this is regular')
    (334.0, 20.25, 'center', Font size=12 weight=normal slant=roman style=None)
    (418.0, 20.25, 'this', Font size=12 weight=normal slant=roman style=None)
    (13.0, 35.25, 'then', Font size=12 weight=normal slant=roman style=None)
    (73.0, 35.25, 'this', Font size=12 weight=normal slant=roman style=None)
    (133.0, 35.25, 'is', Font size=12 weight=normal slant=roman style=None)
    (169.0, 35.25, 'regular', Font size=12 weight=normal slant=roman style=None)
