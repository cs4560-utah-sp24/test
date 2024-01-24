Tests for WBE Chapter 2 Exercise `Line Breaks`
==============================================

Testing boilerplate:

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> _ = wbemocks.patch_canvas()
    >>> import browser

Doctest note
------------

The following tests use a feature of doctest that allows matching
  arbitrary text.
This is so that these tests can specify only part of the output.
An ellipse, `...`,  in the _output_ will match any text.
We use this since your browser may or may not specify a font depending on if
  the zoom exercise is complete.

    >>> print("My name is Inigo Montoya")
    My name is ...
    >>> print("My name is Inigo Montoya")
    My ... Montoya


Testing `resize`
------------------

Let's override text spacing to make it easy to do math
when testing:

	>>> browser.set_parameters(HSTEP=1, VSTEP=1)

Let's mock a URL to load:

    >>> url = 'http://wbemocks.test/chapter2-example3'
    >>> wbemocks.socket.respond_200(url=url,
    ...   body=("u\r\n" +
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
    ...   body=("u\r\n" +
    ...         "\r\n" +
    ...         "\r\n" +
    ...         "d"))
    >>> this_browser.load(browser.URL(url))
    create_text: x=1 y=1 text=u...
    create_text: x=1 y=7 text=d...
