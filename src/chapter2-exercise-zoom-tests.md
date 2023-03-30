Tests for WBE Chapter 2 Exercise `Zoom`
==============================================

Testing boilerplate:

    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> _ = test.patch_canvas()
    >>> import browser

Testing `resize`
------------------

To allow testing of your zoom functionality make sure to handle the `-` and `+` keys
with methods named `zoomout` and `zoomin`, respectively.

The font size should start at 16. When you zoom in, the font size should double, and when you zoom out it should halve.
Be careful: in Tk, the font size must always be an integer, and in Python division always returns a float.
So after doubling or halving the font size, call `int` on the result to make sure it is an integer.

Reset text spacing and line width in case this is run in series with the other
tests.

    >>> browser.WIDTH = 800
    >>> browser.HEIGHT = 600
    >>> browser.HSTEP = 13
    >>> browser.VSTEP = 18

Let's mock a URL to load:

    >>> url = 'http://test.test/chapter2-example7'
    >>> test.socket.respond_200(url=url,
    ...   body="ab")

Loading that URL results in displaying text at size 16:

    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    create_text: x=13 y=18 text=a font=Font size=16 weight=None slant=None style=None anchor=None
    create_text: x=26 y=18 text=b font=Font size=16 weight=None slant=None style=None anchor=None

Calling `zoomout` should make the font size 8, and the gaps between words should halve as well.

    >>> this_browser.zoomout({})
    create_text: x=6 y=9 text=a font=Font size=8 weight=None slant=None style=None anchor=None
    create_text: x=12 y=9 text=b font=Font size=8 weight=None slant=None style=None anchor=None

Calling `zoomin` should restore the default output.

    >>> this_browser.zoomin({})
    create_text: x=12 y=18 text=a font=Font size=16 weight=None slant=None style=None anchor=None
    create_text: x=24 y=18 text=b font=Font size=16 weight=None slant=None style=None anchor=None

Calling `zoomin` again should make the font size 32, make the gaps between letter huge.

    >>> this_browser.zoomin({})
    create_text: x=24 y=36 text=a font=Font size=32 weight=None slant=None style=None anchor=None
    create_text: x=48 y=36 text=b font=Font size=32 weight=None slant=None style=None anchor=None

Scrolling while zoomed
---------------------

Change the line width and scroll step

    >>> browser.WIDTH = 39
    >>> browser.SCROLL_STEP = 38

Let's mock a URL and load it:

    >>> url = 'http://test.test/chapter2-example8'
    >>> test.socket.respond_200(url=url,
    ...   body="abcd")
    >>> this_browser.load(url)
    create_text: x=24 y=36 text=a font=Font size=32 weight=None slant=None style=None anchor=None
    create_text: x=24 y=72 text=b font=Font size=32 weight=None slant=None style=None anchor=None
    create_text: x=24 y=108 text=c font=Font size=32 weight=None slant=None style=None anchor=None
    create_text: x=24 y=144 text=d font=Font size=32 weight=None slant=None style=None anchor=None

Scroll down

    >>> this_browser.scrolldown({})
    create_text: x=24 y=-2 text=a font=Font size=32 weight=None slant=None style=None anchor=None
    create_text: x=24 y=34 text=b font=Font size=32 weight=None slant=None style=None anchor=None
    create_text: x=24 y=70 text=c font=Font size=32 weight=None slant=None style=None anchor=None
    create_text: x=24 y=106 text=d font=Font size=32 weight=None slant=None style=None anchor=None
    
Again

    >>> this_browser.scrolldown({})
    create_text: x=24 y=-4 text=b font=Font size=32 weight=None slant=None style=None anchor=None
    create_text: x=24 y=32 text=c font=Font size=32 weight=None slant=None style=None anchor=None
    create_text: x=24 y=68 text=d font=Font size=32 weight=None slant=None style=None anchor=None
