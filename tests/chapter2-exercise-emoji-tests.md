Tests for WBE Chapter 2 Exercise `Emoji`
========================================

Add support for emoji to your browser. Emoji are characters, and you
can call `create_text` to draw them, but the results aren’t very good.
Instead, head to the OpenMoji project, download the emoji for
“grinning face” as a PNG file, resize it to 16x16 pixels, and save it
to the same folder as the browser. Use Tk’s `PhotoImage` class to load
the image and then the `create_image` method to draw it to the canvas.
~~In fact, download the whole OpenMoji library (look for the “Get
OpenMojis” button at the top right)--then your browser can look up
whatever emoji is used in the page.~~

You only need to handle the grinning face emoji. It is a single
character that you can refer to as `\N{GRINNING FACE}` in Python. It's
best to test the browser directly before running the tests.

This exercise has a few difficult pieces:

- Download the OpenMoji 72x72 PNG images and call the resulting folder
  of emoji images `openmoji`, placed in the same directory as `browser.py`
  The grinning face emoji is in `1F600.png`.

- Resize the emoji images to 16x16 manually. When you do so, overwrite
  the original file so that it's still called `1F600.png`.
  (Technically there are also `zoom` and `subsample` methods on
  `PhotoImage` objects but they are hard to use and work poorly.)

- When you create a `PhotoImage` object, you need to make sure that it
  is not garbage collected. If it is garbage collected, it won't show
  up on the screen. You can do this by storing the `PhotoImage` in a
  field on your `Browser` or in a global.

- Make sure to draw the emoji in the right place!

- If you have a really old Python, you might need to convert the emoji
  picture to GIF for the image to show up, but your Python is probably
  not that old.

For these tests, you only need to handle the "Grinning Face" emoji,
not any others (though you're free to handle others if you'd like).

Tests
-----

Testing boilerplate; hiding `create_rectangle` because of scrollbar tests:

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> _ = wbemocks.patch_canvas()
    >>> import browser
    >>> wbemocks.tkinter.Canvas.hide_command("create_rectangle")

We make the window small and create a test page with several grinning
faces.

	>>> browser.set_parameters(WIDTH=4, HEIGHT=4, VSTEP=1, HSTEP=1, SCROLL_STEP=4)
    >>> wbemocks.tkinter.Canvas.require_image_size(16, 16)
    >>> url = 'http://wbemocks.test/chapter2-example6'
    >>> wbemocks.socket.respond_200(url=url,
    ...   body="Hi \N{Grinning Face} and our \N{Grinning Face}")
	>>> b = browser.Browser()
	>>> url = browser.URL(url)

Let's see what it looks like:

    >>> b.load(url)
    create_text: x=1 y=1 text=H
    create_text: x=2 y=1 text=i
    create_oval: x=2 y=2 image=PhotoImage('openmoji/1F600.png')
    create_text: x=2 y=3 text=a
    create_text: x=1 y=4 text=n
    create_text: x=2 y=4 text=d

Now let's scroll down and see the next smiley:

    >>> b.scrolldown({})
    create_text: x=2 y=-1 text=a
    create_text: x=1 y=0 text=n
    create_text: x=2 y=0 text=d
    create_text: x=2 y=1 text=o
    create_text: x=1 y=2 text=u
    create_text: x=2 y=2 text=r
    create_image: x=2 y=3 image=PhotoImage('openmoji/1F600.png')
