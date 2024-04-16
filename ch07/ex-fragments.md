Tests for WBE Chapter 7 Exercise `Fragments`
=======================

URLs can contain a fragment, which comes at the end of a URL and is
separated from the path by a hash sign `#`. When the browser navigates
to a URL with a fragment, it should scroll the page so that the
element with that identifier is at the top of the screen. Also,
implement fragment links: relative URLs that begin with a `#` don’t
load a new page, but instead scroll the element with that identifier
to the top of the screen. The table of contents on this page uses
fragment links.

You'll want to parse the fragment in the `URL` constructor and add it
to the printed output, like this:

Clicking a fragment link should update the displayed URL in the address bar,
scrolling the identified element to the screen's top.

```
class URL:
    def __repr__(self):
        fragment_part = "" if self.fragment == None else ", fragment=" + self.fragment
        return "URL(scheme={}, host={}, port={}, path={!r}{})".format(
            self.scheme, self.host, self.port, self.path, fragment_part)
```

When you click a fragment link, the URL of the tab (for example, as
shown in the address bar) needs to update. We do not care what happens
when a fragment link is middle clicked; it is not tested.


Test code
---------

Boilerplate.

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> _ = wbemocks.patch_canvas()
    >>> import browser
    >>> this_browser = browser.Browser()
    >>> this_browser.chrome.bottom
    60
    >>> wbemocks.MockCanvas.hide_above(60)

Shorten window

    >>> browser.set_parameters(HEIGHT=200)

Let's make a fragment URL and make sure it prints correctly

    >>> body = ('<h1 id="start">Start</h1>' +
    ...         '<p>' + 'a<br>'*15 + '</p>' +
    ...         '<h1 id="target">Target</h1>' +
    ...         '<p>' + 'b<br>'*40 + '</p>' +
    ...         'Bottom text')
    >>> url = browser.URL(wbemocks.socket.serve(body) + "#target")
    >>> url
    URL(scheme=http, host=test, port=80, path='/0', fragment=target)
    >>> str(url)
    'http://test/0#target'

Let's load it:
    
    >>> this_browser.new_tab(url)
    create_text: x=13 y=62.25 text=Target font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=77.25 text=b font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=92.25 text=b font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=107.25 text=b font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=122.25 text=b font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=137.25 text=b font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=152.25 text=b font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=167.25 text=b font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=182.25 text=b font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=197.25 text=b font=Font size=12 weight=normal slant=roman style=None anchor=nw

    >>> this_browser.tabs[0].url
    URL(scheme=http, host=test, port=80, path='/0', fragment=target)
    >>> this_browser.tabs[0].scroll
    258.0

Test clicking on a link with an absolute path including a fragment.

    >>> body = (f'<a href="{url}">Full path link</a><br>'
    ...         + 'c<br>'*20
    ...         + '<h1 id="fullpath">Full path target</h1>'
    ...         + 'd<br>'*40
    ...         + 'Bottom text')
    >>> url = browser.URL(wbemocks.socket.serve(body))
    >>> this_browser = browser.Browser()
    >>> this_browser.new_tab(url)
    create_text: x=13 y=80.25 text=Full font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=73 y=80.25 text=path font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=133 y=80.25 text=link font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=95.25 text=c font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=110.25 text=c font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=125.25 text=c font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=140.25 text=c font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=155.25 text=c font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=170.25 text=c font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=185.25 text=c font=Font size=12 weight=normal slant=roman style=None anchor=nw

    >>> this_browser.tabs[0].url
    URL(scheme=http, host=test, port=80, path='/1')
    >>> this_browser.tabs[0].scroll
    0

    >>> this_browser.handle_click(wbemocks.ClickEvent(14, 81))
    create_text: x=13 y=62.25 text=Target font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=77.25 text=b font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=92.25 text=b font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=107.25 text=b font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=122.25 text=b font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=137.25 text=b font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=152.25 text=b font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=167.25 text=b font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=182.25 text=b font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=197.25 text=b font=Font size=12 weight=normal slant=roman style=None anchor=nw

    >>> this_browser.tabs[0].url
    URL(scheme=http, host=test, port=80, path='/0', fragment=target)
    >>> this_browser.tabs[0].scroll
    258.0

Test clicking on a link with a relative fragment.
This should only scroll the existing page, and not reload the contents of the
  page.

    >>> body = ('<a href="#relpath">Relative path link</a><br>'
    ...         + 'e<br>'*19
    ...         + '<h1 id="relpath">Relative path target</h1>'
    ...         + 'f<br>'*60
    ...         + 'Bottom text')
    >>> url = browser.URL(wbemocks.socket.serve(body))
    >>> this_browser = browser.Browser()

    >>> this_browser.new_tab(url)
    create_text: x=13 y=80.25 text=Relative font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=121 y=80.25 text=path font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=181 y=80.25 text=link font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=95.25 text=e font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=110.25 text=e font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=125.25 text=e font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=140.25 text=e font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=155.25 text=e font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=170.25 text=e font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=185.25 text=e font=Font size=12 weight=normal slant=roman style=None anchor=nw

    >>> this_browser.tabs[0].url
    URL(scheme=http, host=test, port=80, path='/2')
    >>> this_browser.tabs[0].scroll
    0

To check that the page is not requested again change the server's response.

    >>> wbemocks.socket.respond_200(url, "Do not load me")

Click on the relative fragment.

    >>> this_browser.handle_click(wbemocks.ClickEvent(14, 81))
    create_text: x=13 y=62.25 text=Relative font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=121 y=62.25 text=path font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=181 y=62.25 text=target font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=77.25 text=f font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=92.25 text=f font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=107.25 text=f font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=122.25 text=f font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=137.25 text=f font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=152.25 text=f font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=167.25 text=f font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=182.25 text=f font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=197.25 text=f font=Font size=12 weight=normal slant=roman style=None anchor=nw

    >>> this_browser.tabs[0].url
    URL(scheme=http, host=test, port=80, path='/2', fragment=relpath)
    >>> this_browser.tabs[0].scroll
    318.0

If the fragment does not exist then don't change the scroll position.

    >>> body = ('<a href="#heyo">Nonexistant fragment</a><br>'
    ...         + 'g<br>'*14
    ...         + '<h1 id="hi">Something</h1>'
    ...         + 'h<br>'*60
    ...         + 'Bottom text')
    >>> url = browser.URL(wbemocks.socket.serve(body))
    >>> this_browser = browser.Browser()

    >>> this_browser.new_tab(url)
    create_text: x=13 y=80.25 text=Nonexistant font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=157 y=80.25 text=fragment font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=95.25 text=g font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=110.25 text=g font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=125.25 text=g font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=140.25 text=g font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=155.25 text=g font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=170.25 text=g font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=185.25 text=g font=Font size=12 weight=normal slant=roman style=None anchor=nw

    >>> this_browser.handle_click(wbemocks.ClickEvent(14, 81))
    create_text: x=13 y=80.25 text=Nonexistant font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=157 y=80.25 text=fragment font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=95.25 text=g font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=110.25 text=g font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=125.25 text=g font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=140.25 text=g font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=155.25 text=g font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=170.25 text=g font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=185.25 text=g font=Font size=12 weight=normal slant=roman style=None anchor=nw

    >>> this_browser.tabs[0].url
    URL(scheme=http, host=test, port=80, path='/3', fragment=heyo)
    >>> this_browser.tabs[0].scroll
    0

Clicking a fragment link when a fragment url is already loaded should
  replace the fragment.

    >>> body = ('<a href="#relpath">Relative path link</a><br>'
    ...         + 'i<br>'*34
    ...         + '<h1 id="relpath">Relative path target</h1>'
    ...         + 'j<br>'*60
    ...         + 'Bottom text')
    >>> url = browser.URL(wbemocks.socket.serve(body) + "#nothere")
    >>> this_browser = browser.Browser()
    >>> this_browser.new_tab(url)
    create_text: x=13 y=80.25 text=Relative font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=121 y=80.25 text=path font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=181 y=80.25 text=link font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=95.25 text=i font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=110.25 text=i font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=125.25 text=i font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=140.25 text=i font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=155.25 text=i font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=170.25 text=i font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=185.25 text=i font=Font size=12 weight=normal slant=roman style=None anchor=nw

    >>> this_browser.handle_click(wbemocks.ClickEvent(14, 81))
    create_text: x=13 y=62.25 text=Relative font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=121 y=62.25 text=path font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=181 y=62.25 text=target font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=77.25 text=j font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=92.25 text=j font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=107.25 text=j font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=122.25 text=j font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=137.25 text=j font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=152.25 text=j font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=167.25 text=j font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=182.25 text=j font=Font size=12 weight=normal slant=roman style=None anchor=nw
    create_text: x=13 y=197.25 text=j font=Font size=12 weight=normal slant=roman style=None anchor=nw

    >>> this_browser.tabs[0].url
    URL(scheme=http, host=test, port=80, path='/4', fragment=relpath)
    >>> int(this_browser.active_tab.scroll)
    543

Ensure fragment identifiers in URLs are differentiated based on case sensitivity during comparison.

    >>> body = ('<h1 id="Fragment">Upper Case Fragment</h1>' +
    ...         'a<br>'*15 +
    ...         '<h1 id="fragment">Lower Case fragment</h1>' +
    ...         'b<br>'*40)
    >>> url = wbemocks.socket.serve(body)

    >>> this_browser.active_tab.load(browser.URL(url + "#fragment"))
    >>> int(this_browser.active_tab.scroll)
    258

    >>> this_browser.active_tab.load(browser.URL(url + "#Fragment"))
    >>> int(this_browser.active_tab.scroll)
    18
