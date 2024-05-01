Tests for WBE Chapter 2 Exercise `Line Breaks`
==============================================

Change `layout` to end the current line and start a new one
when it sees a newline character. Increment `y` by more than
`VSTEP` to give the illusion of paragraph breaks. There are
poems embedded in "Journey to the West"; now you’ll be able
to make them out.

Specifically, detect the `\n` character and add a line break.

(Side note: The difference between `\n` and `\r\n` stems from old
typewriter mechanisms. `\n` (line feed) moves down to a new line,
while `\r` (carriage return) moves the carriage to the beginning of
the line. `\r\n`, combining both, is used in some systems (like
Windows) to start a new line.)

Tests
-----

Testing boilerplate:

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> _ = wbemocks.patch_canvas()
    >>> import browser


Let's override text spacing to make it easy to do math
when testing:

	>>> browser.set_parameters(HSTEP=1, VSTEP=1)

Let's mock a URL to load:

    >>> url = 'http://wbemocks.test/chapter2-example3'
    >>> wbemocks.socket.respond_200(url=url,
    ...   body=("u\n" +
    ...         "d"))

Create a browser instance and load the url.
Even though the visible text could fit on one line it is split into two.
Note that the newline characters are not present in the output,
  but instead cause the text to be moved down by twice the `VSTEP`

    >>> this_browser = browser.Browser()
    >>> this_browser.load(browser.URL(url))
    create_text: x=1 y=1 text=u
    create_text: x=1 y=3 text=d

Each additional newline moves the text down by twice `VSTEP`

    >>> url = 'http://wbemocks.test/chapter2-example4'
    >>> wbemocks.socket.respond_200(url=url,
    ...   body=("u\n" +
    ...         "\n" +
    ...         "\n" +
    ...         "d"))
    >>> this_browser.load(browser.URL(url))
    create_text: x=1 y=1 text=u
    create_text: x=1 y=7 text=d

Make sure that `cursor_x` is reset on a line break:

    >>> url = 'http://wbemocks.test/cursor-reset-test'
    >>> wbemocks.socket.respond_200(url=url, body="eren\nmika")
    >>> this_browser = browser.Browser()
    >>> this_browser.load(browser.URL(url))
    create_text: x=1 y=1 text=e
    create_text: x=2 y=1 text=r
    create_text: x=3 y=1 text=e
    create_text: x=4 y=1 text=n
    create_text: x=1 y=3 text=m
    create_text: x=2 y=3 text=i
    create_text: x=3 y=3 text=k
    create_text: x=4 y=3 text=a

