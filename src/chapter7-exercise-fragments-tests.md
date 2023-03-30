Tests for WBE Chapter 7 Exercise `Fragments`
=======================

Description
-----------

URLs can contain a fragment, which comes at the end of a URL and is separated
  from the path by a hash sign #.
When the browser navigates to a URL with a fragment, it should scroll the page
  so that the element with that identifier is at the top of the screen.
Also, implement fragment links: relative URLs that begin with a # don’t load a
  new page, but instead scroll the element with that identifier to the top of
  the screen.
The table of contents on this page uses fragment links.


Extra Requirements
------------------
* We do not care what happens when middle clicking a relative fragment and it
  will not be tested.


Test code
---------

Boilerplate.

    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> _ = test.patch_skip_chrome_canvas()
    >>> test.NORMALIZE_FONT = True
    >>> import browser

Shorten window

    >>> browser.HEIGHT = 200

Test loading a url with a fragment.

    >>> url = 'http://test.test/chapter7-fragment1'
    >>> body = ('<h1 id="start">Start</h1>'
    ...         + 'a<br>'*15
    ...         + '<h1 id="target">Target</h1>'
    ...         + 'b<br>'*40
    ...         + 'Bottom text')
    >>> test.socket.respond_200(url, body)
    >>> this_browser = browser.Browser()

    >>> this_browser.load(url + "#target")
    create_text: x=13 y=102.25 text=Target font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=117.25 text=b font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=132.25 text=b font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=147.25 text=b font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=162.25 text=b font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=177.25 text=b font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=192.25 text=b font=Font size=12 weight=normal slant=roman style=None anchor=nw

    >>> this_browser.tabs[0].url
    'http://test.test/chapter7-fragment1#target'

    >>> this_browser.tabs[0].scroll
    258.0

Test clicking on a link with an absolute path including a fragment.

    >>> url = 'http://test.test/chapter7-fragment3'
    >>> body = (f'<a href="{url}#fullpath">Full path link</a>'
    ...         + 'c<br>'*20
    ...         + '<h1 id="fullpath">Full path target</h1>'
    ...         + 'd<br>'*40
    ...         + 'Bottom text')
    >>> test.socket.respond_200(url, body)
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    create_text: x=13 y=120.25 text=Full font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=73 y=120.25 text=path font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=133 y=120.25 text=link font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=135.25 text=c font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=150.25 text=c font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=165.25 text=c font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=180.25 text=c font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=195.25 text=c font=Font size=12 weight=normal slant=roman style=None anchor=nw

    >>> this_browser.handle_click(test.Event(14, 121))
    create_text: x=13 y=102.25 text=Full font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=73 y=102.25 text=path font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=133 y=102.25 text=target font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=117.25 text=d font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=132.25 text=d font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=147.25 text=d font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=162.25 text=d font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=177.25 text=d font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=192.25 text=d font=Font size=12 weight=normal slant=roman style=None anchor=nw

    >>> this_browser.tabs[0].url
    'http://test.test/chapter7-fragment3#fullpath'

    >>> this_browser.tabs[0].scroll
    333.0

Test clicking on a link with a relative fragment.
This should only scroll the existing page, and not reload the contents of the
  page.

    >>> url = 'http://test.test/chapter7-fragment4'
    >>> body = ('<a href="#relpath">Relative path link</a>'
    ...         + 'e<br>'*19
    ...         + '<h1 id="relpath">Relative path target</h1>'
    ...         + 'f<br>'*60
    ...         + 'Bottom text')
    >>> test.socket.respond_200(url, body)
    >>> this_browser = browser.Browser()

    >>> this_browser.load(url)
    create_text: x=13 y=120.25 text=Relative font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=121 y=120.25 text=path font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=181 y=120.25 text=link font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=135.25 text=e font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=150.25 text=e font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=165.25 text=e font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=180.25 text=e font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=195.25 text=e font=Font size=12 weight=normal slant=roman style=None anchor=nw

To check that the page is not requested again change the server's response.

    >>> test.socket.respond_200(url, "Do not load me")

Click on the relative fragment.

    >>> this_browser.handle_click(test.Event(14, 121))
    create_text: x=13 y=102.25 text=Relative font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=121 y=102.25 text=path font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=181 y=102.25 text=target font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=117.25 text=f font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=132.25 text=f font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=147.25 text=f font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=162.25 text=f font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=177.25 text=f font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=192.25 text=f font=Font size=12 weight=normal slant=roman style=None anchor=nw

    >>> this_browser.tabs[0].url
    'http://test.test/chapter7-fragment4#relpath'

    >>> this_browser.tabs[0].scroll
    318.0

If the fragment does not exist then don't change the scroll position.

    >>> url = 'http://test.test/chapter7-fragment5'
    >>> body = ('<a href="#heyo">Nonexistant fragment</a>'
    ...         + 'g<br>'*14
    ...         + '<h1 id="hi">Something</h1>'
    ...         + 'h<br>'*60
    ...         + 'Bottom text')
    >>> test.socket.respond_200(url, body)
    >>> this_browser = browser.Browser()

    >>> this_browser.load(url)
    create_text: x=13 y=120.25 text=Nonexistant font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=157 y=120.25 text=fragment font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=135.25 text=g font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=150.25 text=g font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=165.25 text=g font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=180.25 text=g font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=195.25 text=g font=Font size=12 weight=normal slant=roman style=None anchor=nw

    >>> this_browser.handle_click(test.Event(14, 121))
    create_text: x=13 y=120.25 text=Nonexistant font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=157 y=120.25 text=fragment font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=135.25 text=g font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=150.25 text=g font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=165.25 text=g font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=180.25 text=g font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=195.25 text=g font=Font size=12 weight=normal slant=roman style=None anchor=nw

    >>> this_browser.tabs[0].url
    'http://test.test/chapter7-fragment5#heyo'

    >>> this_browser.tabs[0].scroll
    0

Clicking a fragment link when a fragment url is already loaded should
  replace the fragment.

    >>> url = 'http://test.test/chapter7-fragment6'
    >>> body = ('<a href="#relpath">Relative path link</a>'
    ...         + 'i<br>'*34
    ...         + '<h1 id="relpath">Relative path target</h1>'
    ...         + 'j<br>'*60
    ...         + 'Bottom text')
    >>> test.socket.respond_200(url, body)
    >>> this_browser = browser.Browser()

    >>> this_browser.load(url + "#nothere")
    create_text: x=13 y=120.25 text=Relative font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=121 y=120.25 text=path font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=181 y=120.25 text=link font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=135.25 text=i font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=150.25 text=i font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=165.25 text=i font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=180.25 text=i font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=195.25 text=i font=Font size=12 weight=normal slant=roman style=None anchor=nw

    >>> this_browser.handle_click(test.Event(14, 121))
    create_text: x=13 y=102.25 text=Relative font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=121 y=102.25 text=path font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=181 y=102.25 text=target font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=117.25 text=j font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=132.25 text=j font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=147.25 text=j font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=162.25 text=j font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=177.25 text=j font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=192.25 text=j font=Font size=12 weight=normal slant=roman style=None anchor=nw

    >>> this_browser.tabs[0].url
    'http://test.test/chapter7-fragment6#relpath'

    >>> this_browser.tabs[0].scroll
    543.0
