Tests for WBE Chapter 5 Exercise `Scrollbar`
=======================

Description
-----------

At the right edge of the screen, draw a blue, rectangular scrollbar. 
The ratio of its height to the screen height should be the same as the ratio of
  the screen height to the document height, and its location should reflect the
  position of the screen within the document. 
Hide the scrollbar if the whole document fits onscreen.

    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> _ = test.patch_canvas()
    >>> import browser

Resize the window and set up the URL and web page, this is the content that we will be examining.


    >>> url = 'http://test.test/chapter5_example6'
    >>> content = "<br>".join(["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"])
    >>> test.socket.respond_200(url, content)

The scrollbar should be a blue rectangle, 8 pixels wide, on the right edge of the canvas.
To make the scrollbar always render on top of other content make sure to draw it last.

    >>> browser.HEIGHT = 118
    >>> browser.SCROLL_STEP = 60
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    create_text: x=13 y=21.0 text=a font=Font size=16 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=41.0 text=b font=Font size=16 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=61.0 text=c font=Font size=16 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=81.0 text=d font=Font size=16 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=101.0 text=e font=Font size=16 weight=normal slant=roman style=None anchor=nw
    create_rectangle: x1=792 y1=0.0 x2=800 y2=59.0 width=0 fill='blue'
    
    >>> this_browser.scrolldown(None)
    create_text: x=13 y=1.0 text=c font=Font size=16 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=21.0 text=d font=Font size=16 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=41.0 text=e font=Font size=16 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=61.0 text=f font=Font size=16 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=81.0 text=g font=Font size=16 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=101.0 text=h font=Font size=16 weight=normal slant=roman style=None anchor=nw
    create_rectangle: x1=792 y1=30.0 x2=800 y2=89.0 width=0 fill='blue'

    >>> this_browser.scrolldown(None)
    create_text: x=13 y=3.0 text=f font=Font size=16 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=23.0 text=g font=Font size=16 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=43.0 text=h font=Font size=16 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=63.0 text=i font=Font size=16 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=83.0 text=j font=Font size=16 weight=normal slant=roman style=None anchor=nw
    create_rectangle: x1=792 y1=59.0 x2=800 y2=118.0 width=0 fill='blue'
    

When the whole document fits onscreen don't draw the scrollbar.

    >>> browser.HEIGHT = 600
    >>> browser.SCROLL_STEP = 100
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    create_text: x=13 y=21.0 text=a font=Font size=16 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=41.0 text=b font=Font size=16 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=61.0 text=c font=Font size=16 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=81.0 text=d font=Font size=16 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=101.0 text=e font=Font size=16 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=121.0 text=f font=Font size=16 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=141.0 text=g font=Font size=16 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=161.0 text=h font=Font size=16 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=181.0 text=i font=Font size=16 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=201.0 text=j font=Font size=16 weight=normal slant=roman style=None anchor=nw
