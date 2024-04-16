Tests for WBE Chapter 2 Exercise `Resizing`
==============================================

Make the browser resizable. To do so, pass the fill and expand
arguments to `canvas.pack`, call and bind to the `<Configure>` event,
which happens when the window is resized. The window’s new width and
height can be found in the width and height fields on the event
object. Remember that when the window is resized, the line breaks must
change, so you will need to call layout again.

Make sure that your `Browser` class handles resize events in a
`resize` method. Do not redownload the page in `resize`.


Tests
-----

Testing boilerplate:

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> _ = wbemocks.patch_canvas()
    >>> import browser

Let's override text spacing and line width to make it easy to do math
when testing:

	>>> browser.set_parameters(WIDTH=1, HSTEP=1, VSTEP=1)

Let's mock a URL to load:

    >>> url = 'http://wbemocks.test/chapter2-example6'
    >>> wbemocks.socket.respond_200(url=url,
    ...   body="abcd")

Loading that URL results in the text with each letter on a new y value.
The `x` value is always one, but `y` increments, since the canvas is of width
 one.

    >>> this_browser = browser.Browser()
    >>> this_browser.load(browser.URL(url))
    create_text: x=1 y=1 text=a
    create_text: x=1 y=2 text=b
    create_text: x=1 y=3 text=c
    create_text: x=1 y=4 text=d

Now we change what `url` points to to make sure we don't redownload
the page when resizing:

    >>> wbemocks.socket.respond_200(url=url,
    ...   body="efgh")

Calling `resize` with a wider window should allow the text to be on one line.
Now all the characters have the same `y`, but different `x` increments.

If you see `efgh` instead of `abcd`, your browser is re-downloading
the page when resizing; don't do that.

    >>> e = wbemocks.ResizeEvent(width=100, height=10)
    >>> this_browser.resize(e)
    create_text: x=1 y=1 text=a
    create_text: x=2 y=1 text=b
    create_text: x=3 y=1 text=c
    create_text: x=4 y=1 text=d

Calling `resize` with a narrower window should split the text across two lines.

    >>> e = wbemocks.ResizeEvent(width=4, height=10)
    >>> this_browser.resize(e)
    create_text: x=1 y=1 text=a
    create_text: x=2 y=1 text=b
    create_text: x=1 y=2 text=c
    create_text: x=2 y=2 text=d
