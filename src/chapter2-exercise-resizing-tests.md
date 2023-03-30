Tests for WBE Chapter 2 Exercise `Resizing`
==============================================

Testing boilerplate:

    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> _ = test.patch_canvas()
    >>> import browser

Testing `resize`
------------------

Make sure that your `Browser` class handles resize events in a `resize` method.

Let's override text spacing and line width to make it easy to do math
when testing:

    >>> browser.WIDTH = 1
    >>> browser.HSTEP = 1
    >>> browser.VSTEP = 1

Let's mock a URL to load:

    >>> url = 'http://test.test/chapter2-example6'
    >>> test.socket.respond_200(url=url,
    ...   body="abcd")

Loading that URL results in the text with each letter on a new y value.
The `x` value is always one, but `y` increments, since the canvas is of width
 one.

    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    create_text: x=1 y=1 text=a...
    create_text: x=1 y=2 text=b...
    create_text: x=1 y=3 text=c...
    create_text: x=1 y=4 text=d...

Calling `resize` with a wider window should allow the text to be on one line.
Now all the characters have the same `y`, but different `x` increments.

    >>> e = test.resize_event(width=100, height=10)
    >>> this_browser.resize(e)
    create_text: x=1 y=1 text=a...
    create_text: x=2 y=1 text=b...
    create_text: x=3 y=1 text=c...
    create_text: x=4 y=1 text=d...

Calling `resize` with a narrower window should split the text across two lines.

    >>> e = test.resize_event(width=4, height=10)
    >>> this_browser.resize(e)
    create_text: x=1 y=1 text=a...
    create_text: x=2 y=1 text=b...
    create_text: x=1 y=2 text=c...
    create_text: x=2 y=2 text=d...
