Tests for WBE Chapter 7 Exercise `Bookmarks`
=======================

Description
-----------

Implement basic bookmarks. Add a button to the browser chrome;
clicking it should bookmark the page. When you’re looking at a
bookmarked page, that bookmark button should look different (maybe
yellow?) to remind the user that the page is bookmarked, and clicking
it should un-bookmark it. Add a special web page, about:bookmarks, for
viewing the list of bookmarks.

The bookmarks button must be 20 pixels wide and as tall as the address
bar. It should be located on the same level and to the right of the
address bar. Add the standard padding on both sides.

- Store the bookmarks button rectangle in the `bookmarks_rect` field
  of the `Chrome`.
- Make sure to shorten the address bar to make room for the bookmarks
  button.
- The button has a black outline and also, if the current page is
  bookmarked, a `yellow` background
- Make sure to draw the background behind the outline.
- You can also draw something, like a star or a B or something, in the
  bookmarks button, but this is not required.

The button should be clickable:

- Store the list of bookmarks in the `bookmarks` field of the
  `Browser`. It should be a list of strings.
- Clicking the button should add the current URL to the bookmarks, or
  remove it if it's already there.

Finally, it should be possible to view the list of bookmarks by going
to `about:bookmarks`.

- You'll need to allow the `about` scheme in the URL parser
- Instead of calling `request` to load the URL, construct the
  bookmarks page HTML

That page should contain bare links for each URL, like this:

```
<!doctype html>
<a href="http://xkcd.com">http://xkcd.com</a><br>
<a href="https://utah.edu">https://utah.edu</a><br>
```


Test code
---------

Boilerplate.

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> _ = wbemocks.patch_silent_canvas()
    >>> import browser

Load the first site.

    >>> url_1 = browser.URL(wbemocks.socket.serve("Site 1"))
    >>> this_browser = browser.Browser()
    >>> this_browser.new_tab(url_1)

This function looks through the calls used on the canvas object and look for a
  rectangle being drawn where indicated above with a white fill.

    >>> wbemocks.check_not_bookmarked()
    True

    >>> this_browser.bookmarks
    []

Load the second site by typing it in.

    >>> url_2 = 'http://site2.com/'
    >>> wbemocks.socket.respond_200(url_2, body="Site 2")

    >>> this_browser.handle_click(wbemocks.ClickEvent(50, 51))
    >>> for c in url_2:
    ...   this_browser.handle_key(wbemocks.KeyEvent(c))
    >>> this_browser.handle_enter(wbemocks.Event())
    >>> this_browser.tabs[0].url
    'http://site2.com/'

Make sure it is not bookmarked.

    >>> wbemocks.check_not_bookmarked()
    True

    >>> browser.BOOKMARKS
    []

Go back to the first site and bookmark it.

    >>> this_browser.tabs[0].go_back()
    >>> this_browser.handle_click(wbemocks.ClickEvent(777, 50))

Check that it got bookmarked.

    >>> wbemocks.check_bookmarked()
    True

    >>> browser.BOOKMARKS
    ['http://site1.com/']

Load the second site by typing it in again.

    >>> this_browser.handle_click(wbemocks.ClickEvent(50, 51))
    >>> for c in url_2:
    ...   this_browser.handle_key(wbemocks.KeyEvent(c))
    >>> this_browser.handle_enter(wbemocks.Event())
    >>> this_browser.tabs[0].url
    'http://site2.com/'

Make sure it is not bookmarked

    >>> wbemocks.check_not_bookmarked()
    True

    >>> browser.BOOKMARKS
    ['http://site1.com/']

Bookmark it and check.

    >>> this_browser.handle_click(wbemocks.ClickEvent(777, 50))

    >>> wbemocks.check_bookmarked()
    True

    >>> browser.BOOKMARKS
    ['http://site1.com/', 'http://site2.com/']

Request the bookmark site directly.

    >>> bk_url = "about:bookmarks"
    >>> headers, body = browser.request(bk_url)
    >>> print(body) #doctest: +NORMALIZE_WHITESPACE
    <!doctype html>
    <a href="http://site1.com/">http://site1.com/</a><br>
    <a href="http://site2.com/">http://site2.com/</a><br>

Unbookmark the second site.

    >>> this_browser.handle_click(wbemocks.ClickEvent(777, 50))

    >>> wbemocks.check_not_bookmarked()
    True

    >>> browser.BOOKMARKS
    ['http://site1.com/']

Request the bookmark site directly.

    >>> bk_url = "about:bookmarks"
    >>> headers, body = browser.request(bk_url)
    >>> print(body) #doctest: +NORMALIZE_WHITESPACE
    <!doctype html>
    <a href="http://site1.com/">http://site1.com/</a><br>
