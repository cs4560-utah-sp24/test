Tests for WBE Chapter 2
=======================

Chapter 2 (Drawing to the Screen) is about how to get text parsed, laid out
and drawn on the screen, plus a very simple implementation of scrolling. This
file contains tests for this functionality.

    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> import browser

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

The layout function takes in text and outputs a display list. It uses WIDTH to
determine the maximum length of a line, HSTEP for the horizontal distance
between letters, and VSTEP for the vertical distance between lines. Each entry
in the display list is of the form (x, y, c), where x is the horizontal offset
to the right, y is the vertical offset downward, and c is the character to
draw.

Let's override those values to convenient ones that make it easy to do math
when testing:

    >>> browser.WIDTH = 11
    >>> browser.HSTEP = 1
    >>> browser.VSTEP = 1

Both of these fit on one line:

    >>> browser.layout("hello")
    [(1, 1, 'h'), (2, 1, 'e'), (3, 1, 'l'), (4, 1, 'l'), (5, 1, 'o')]
    >>> browser.layout("hello mom")
    [(1, 1, 'h'), (2, 1, 'e'), (3, 1, 'l'), (4, 1, 'l'), (5, 1, 'o'), (6, 1, ' '), (7, 1, 'm'), (8, 1, 'o'), (9, 1, 'm')]

This does not though (notice that the 's' has a 2 in the y coordinate):

    >>> browser.layout("hello moms")
    [(1, 1, 'h'), (2, 1, 'e'), (3, 1, 'l'), (4, 1, 'l'), (5, 1, 'o'), (6, 1, ' '), (7, 1, 'm'), (8, 1, 'o'), (9, 1, 'm'), (1, 2, 's')]


Testing `Browser`
-----------------

The Browser class defines a simple web browser, with methods to load,
draw to the screen, and scroll down.

Testing `Browser.load`
----------------------

Let's first mock a URL to load:

    >>> url = 'http://test.test/chapter2-example1'
    >>> test.socket.respond(url=url,
    ...   response=("HTTP/1.0 200 OK\r\n" +
    ...             "Header1: Value1\r\n"
    ...             "\r\n" +
    ...             "Body text").encode())

Loading that URL results in a display list:

    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    >>> this_browser.display_list
    [(1, 1, 'B'), (2, 1, 'o'), (3, 1, 'd'), (4, 1, 'y'), (5, 1, ' '), (6, 1, 't'), (7, 1, 'e'), (8, 1, 'x'), (9, 1, 't')]


Testing `Browser.scrolldown`
----------------------------

Let's install a mock canvas that prints out the x and y coordinates, plus
the text drawn:

    >>> test.patch_canvas()
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    create_text: x=1 y=1 text=B...
    create_text: x=2 y=1 text=o...
    create_text: x=3 y=1 text=d...
    create_text: x=4 y=1 text=y...
    create_text: x=6 y=1 text=t...
    create_text: x=7 y=1 text=e...
    create_text: x=8 y=1 text=x...
    create_text: x=9 y=1 text=t...

SCROLL_STEP configures how much to scroll by each time. Let's set it to
a convenient value:

    >>> browser.SCROLL_STEP = browser.VSTEP + 2

After scrolling, all of the text is off screen, so no text is output to the
canvas:

    >>> this_browser.scrolldown({})

Now let's load a different URL that provides three lines of text:

    >>> url = 'http://test.test/chapter2-example2'
    >>> test.socket.respond(url=url,
    ...   response = ("HTTP/1.0 200 OK\r\n" +
    ...               "Header1: Value1\r\n" +
    ...               "\r\n" +
    ...               "Body text that is longer").encode())
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    create_text: x=1 y=1 text=B...
    create_text: x=2 y=1 text=o...
    create_text: x=3 y=1 text=d...
    create_text: x=4 y=1 text=y...
    create_text: x=6 y=1 text=t...
    create_text: x=7 y=1 text=e...
    create_text: x=8 y=1 text=x...
    create_text: x=9 y=1 text=t...
    create_text: x=2 y=2 text=t...
    create_text: x=3 y=2 text=h...
    create_text: x=4 y=2 text=a...
    create_text: x=5 y=2 text=t...
    create_text: x=7 y=2 text=i...
    create_text: x=8 y=2 text=s...
    create_text: x=1 y=3 text=l...
    create_text: x=2 y=3 text=o...
    create_text: x=3 y=3 text=n...
    create_text: x=4 y=3 text=g...
    create_text: x=5 y=3 text=e...
    create_text: x=6 y=3 text=r...

Scrolling down will now still show some of the text on-screen, because it took
up three lines, not just one:

    >>> this_browser.scrolldown({})
    create_text: x=2 y=-1 text=t...
    create_text: x=3 y=-1 text=h...
    create_text: x=4 y=-1 text=a...
    create_text: x=5 y=-1 text=t...
    create_text: x=7 y=-1 text=i...
    create_text: x=8 y=-1 text=s...
    create_text: x=1 y=0 text=l...
    create_text: x=2 y=0 text=o...
    create_text: x=3 y=0 text=n...
    create_text: x=4 y=0 text=g...
    create_text: x=5 y=0 text=e...
    create_text: x=6 y=0 text=r...
