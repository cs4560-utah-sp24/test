Tests for WBE Chapter 7 Exercise `Bookmarks`
=======================

Description
-----------

Implement basic bookmarks.
Add a button to the browser chrome; clicking it should bookmark the page.
When you’re looking at a bookmarked page, that bookmark button should look
  different (maybe yellow?) to remind the user that the page is bookmarked,
  and clicking it should un-bookmark it.
Add a special web page, about:bookmarks, for viewing the list of bookmarks.


Extra Requirements
------------------

* The button will be located on the right hand side of the chrome on level with
  the address bar.
  - This will require shortening the address bar's rectangle and clickable area
    by 30 pixels (i.e. the right side shrinks from `WIDTH - 10` to `WIDTH - 40`)
  - The button's bounding rectangle will be from x = `WIDTH - 35` to
    x = `WIDTH - 10`, and y = `50` to y = `90`.
  - When the viewed page is in the `BOOKMARKS` list draw the rectangle with
    yellow fill, and draw it with a white fill otherwise
  - You can add a "B" at `WIDTH - 31`, `52` to make the bookmark button look
    nicer, but this will not be tested.
* The list of bookmarked pages should be held in a global named `BOOKMARKS`
* When `request` is given "about:bookmarks" the return should be a tuple of
  an empty dictionary (in place of headers) and the source to the bookmarks page
  - This page is simply bare links with breaks in between separated by
    newlines.
  - The link href and content are both the url, for instance if the bookmarks
    list contained `['http://xkcd.com', 'https://utah.edu']` then the web site
    body would be
    ```
    <!doctype html>
    <a href="http://xkcd.com">http://xkcd.com</a><br>
    <a href="https://utah.edu">https://utah.edu</a><br>
    ```


Test code
---------

Boilerplate.

    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> _ = test.patch_silent_canvas()
    >>> import browser

Load the first site.

    >>> url_1 = 'http://site1.com/'
    >>> test.socket.respond_200(url_1, body="Site 1")
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url_1)

This function looks through the calls used on the canvas object and look for a
  rectangle being drawn where indicated above with a white fill.

    >>> test.check_not_bookmarked()
    True

    >>> browser.BOOKMARKS
    []

Load the second site by typing it in.

    >>> url_2 = 'http://site2.com/'
    >>> test.socket.respond_200(url_2, body="Site 2")

    >>> this_browser.handle_click(test.Event(50, 51))
    >>> for c in url_2:
    ...   this_browser.handle_key(test.key_event(c))
    >>> this_browser.handle_enter(test.enter_event())
    >>> this_browser.tabs[0].url
    'http://site2.com/'

Make sure it is not bookmarked.

    >>> test.check_not_bookmarked()
    True

    >>> browser.BOOKMARKS
    []

Go back to the first site and bookmark it.

    >>> this_browser.tabs[0].go_back()
    >>> this_browser.handle_click(test.Event(777, 50))

Check that it got bookmarked.

    >>> test.check_bookmarked()
    True

    >>> browser.BOOKMARKS
    ['http://site1.com/']

Load the second site by typing it in again.

    >>> this_browser.handle_click(test.Event(50, 51))
    >>> for c in url_2:
    ...   this_browser.handle_key(test.key_event(c))
    >>> this_browser.handle_enter(test.enter_event())
    >>> this_browser.tabs[0].url
    'http://site2.com/'

Make sure it is not bookmarked

    >>> test.check_not_bookmarked()
    True

    >>> browser.BOOKMARKS
    ['http://site1.com/']

Bookmark it and check.

    >>> this_browser.handle_click(test.Event(777, 50))

    >>> test.check_bookmarked()
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

    >>> this_browser.handle_click(test.Event(777, 50))

    >>> test.check_not_bookmarked()
    True

    >>> browser.BOOKMARKS
    ['http://site1.com/']

Request the bookmark site directly.

    >>> bk_url = "about:bookmarks"
    >>> headers, body = browser.request(bk_url)
    >>> print(body) #doctest: +NORMALIZE_WHITESPACE
    <!doctype html>
    <a href="http://site1.com/">http://site1.com/</a><br>
