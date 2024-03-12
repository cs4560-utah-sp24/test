Tests for WBE Chapter 2 Exercise `Scrollbar`
=======================

We'll only implement a subset of a real browser's scrollbar functionality. Specifically:

- You don't have to make the text narrower on the page. Instead, just make sure the scrollbar is positioned over any text.
- You don't have to prevent scrolling past the bottom of the page. Just make sure the scrollbar is correctly positioned when the user is not past the bottom of the page.

Tests
-----

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> _ = wbemocks.patch_canvas()
    >>> import browser

Resize the window and set up the URL and web page:


    >>> url = 'http://wbemocks.test/chapter5_example6'
    >>> content = "abcdefghij"
    >>> wbemocks.socket.respond_200(url, content)
    >>> browser.set_parameters(WIDTH=800, HEIGHT=100,
    ...     VSTEP=20, HSTEP=800, SCROLL_STEP=25)

Since the h-step is equal to the width and the page contents is 10
letters, there should be 10 lines of text. Since each line is 20
pixels tall, the page is a total of 200 pixels tall. Only 100 pixels
appears on the screen at once, so the scrollbar should be 50 pixels
tall.

The scrollbar should be a blue rectangle, 8 pixels wide, on the right
edge of the canvas. To make the scrollbar always renders on top of
other content make sure to draw it last.

    >>> this_browser = browser.Browser()
    >>> this_browser.load(browser.URL(url))
    create_text: x=800 y=20 text=a
    create_text: x=800 y=40 text=b
    create_text: x=800 y=60 text=c
    create_text: x=800 y=80 text=d
    create_text: x=800 y=100 text=e
    create_rectangle: x1=792 y1=0 x2=800 y2=50 width=0 fill='blue'

Scrolling down should move the contents and the rectangle. Note that
we scrolled by 25 pixels, so by 1/8 the height of the page, so the
scrollbar should start at 12.5 pixels and end at 62.5 pixels:
    
    >>> this_browser.scrolldown(None)
    create_text: x=800 y=-5 text=a
    create_text: x=800 y=15 text=b
    create_text: x=800 y=35 text=c
    create_text: x=800 y=55 text=d
    create_text: x=800 y=75 text=e
    create_text: x=800 y=95 text=f
    create_rectangle: x1=792 y1=12.5 x2=800 y2=62.5 width=0 fill='blue'

Scrolling down once more should again move the contents and the rectangle:
    
    >>> this_browser.scrolldown(None)
    create_text: x=800 y=-10 text=b
    create_text: x=800 y=10 text=c
    create_text: x=800 y=30 text=d
    create_text: x=800 y=50 text=e
    create_text: x=800 y=70 text=f
    create_text: x=800 y=90 text=g
    create_rectangle: x1=792 y1=25 x2=800 y2=75 width=0 fill='blue'

When the whole document fits on the screen, don't draw the scrollbar.

	>>> browser.set_parameters(HEIGHT=600)
    >>> this_browser = browser.Browser()
    >>> this_browser.load(browser.URL(url))
    create_text: x=800 y=20 text=a
    create_text: x=800 y=40 text=b
    create_text: x=800 y=60 text=c
    create_text: x=800 y=80 text=d
    create_text: x=800 y=100 text=e
    create_text: x=800 y=120 text=f
    create_text: x=800 y=140 text=g
    create_text: x=800 y=160 text=h
    create_text: x=800 y=180 text=i
    create_text: x=800 y=200 text=j
