Tests for WBE Chapter 2
=======================

Chapter 2 (Drawing to the Screen) is about how to get text parsed, laid out
and drawn on the screen, plus a very simple implementation of scrolling. This
file contains tests for this functionality.

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> import browser
	
Please copy this `set_parameters` function into your browser:

``` {.python}
def set_parameters(**params):
	global WIDTH, HEIGHT, HSTEP, VSTEP, SCROLL_STEP
	if "WIDTH" in params: WIDTH = params["WIDTH"]
	if "HEIGHT" in params: HEIGHT = params["HEIGHT"]
	if "HSTEP" in params: HSTEP = params["HSTEP"]
	if "VSTEP" in params: VSTEP = params["VSTEP"]
	if "SCROLL_STEP" in params: SCROLL_STEP = params["SCROLL_STEP"]
```

If you'd like to define these constants in some other file, you can do
that by modifying this function definition.

Testing `lex`
-------------

The `lex` function is the same as `show` from chapter 1, but now it returns
  the result instead of printing it.

    >>> s = browser.lex('<body>hello</body>')
    >>> s
    'hello'
    >>> s = browser.lex('<body><wbr>hello</body>')
    >>> s
    'hello'
    >>> s = browser.lex('<body>he<wbr>llo</body>')
    >>> s
    'hello'
    >>> s = browser.lex('<body>hel<div>l</div>o</body>')
    >>> s
    'hello'

Note that the tags do not have to match:

    >>> s = browser.lex('<body><p>hel</div>lo</body>')
    >>> s
    'hello'
    >>> s = browser.lex('<body>h<p>el<div>l</p>o</div></body>')
    >>> s
    'hello'

Newlines should not be removed:

    >>> s = browser.lex('<body>hello\nworld</body>')
    >>> s
    'hello\nworld'


Testing `layout`
----------------

The layout function takes in text and outputs a display list. It uses `WIDTH` to
determine the maximum length of a line, `HSTEP` for the horizontal distance
between letters, and `VSTEP` for the vertical distance between lines. Each entry
in the display list is of the form `(x, y, c)`, where `x` is the horizontal offset
to the right, `y` is the vertical offset downward, and `c` is the character to
draw.

Let's override those values to convenient ones that make it easy to do math
when testing:

	>>> browser.set_parameters(WIDTH=11, HSTEP=1, VSTEP=1)

Both of these fit on one line:

    >>> browser.layout("hello")
    [(1, 1, 'h'), (2, 1, 'e'), (3, 1, 'l'), (4, 1, 'l'), (5, 1, 'o')]
    >>> browser.layout("hello mom")
    [(1, 1, 'h'), (2, 1, 'e'), (3, 1, 'l'), (4, 1, 'l'), (5, 1, 'o'), (6, 1, ' '), (7, 1, 'm'), (8, 1, 'o'), (9, 1, 'm')]

This does not though (notice that the `'s'` has a 2 in the `y` coordinate):

    >>> browser.layout("hello moms")
    [(1, 1, 'h'), (2, 1, 'e'), (3, 1, 'l'), (4, 1, 'l'), (5, 1, 'o'), (6, 1, ' '), (7, 1, 'm'), (8, 1, 'o'), (9, 1, 'm'), (1, 2, 's')]


Testing `Browser`
-----------------

The Browser class defines a simple web browser, with methods to load,
draw to the screen, and scroll down.

Let's first mock a URL to load:

    >>> url = 'http://wbemocks.test/chapter2-example1'
    >>> wbemocks.socket.respond(url=url,
    ...   response=("HTTP/1.0 200 OK\r\n" +
    ...             "Header1: Value1\r\n"
    ...             "\r\n" +
    ...             "Body text").encode())

Loading that URL results in a display list:

    >>> this_browser = browser.Browser()
    >>> this_browser.load(browser.URL(url))
    >>> this_browser.display_list
    [(1, 1, 'B'), (2, 1, 'o'), (3, 1, 'd'), (4, 1, 'y'), (5, 1, ' '), (6, 1, 't'), (7, 1, 'e'), (8, 1, 'x'), (9, 1, 't')]
