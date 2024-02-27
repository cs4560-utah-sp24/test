Tests for WBE Chapter 7 Exercise `Bookmarks`
=======================

Description
-----------

Implement basic bookmarks. Add a button to the browser chrome;
clicking it should bookmark the page. When you’re looking at a
bookmarked page, that bookmark button should look different (maybe
yellow?) to remind the user that the page is bookmarked, and clicking
it should un-bookmark it. Add a special web page, `about:bookmarks`, for
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
to `about://bookmarks`. This isn't quite what the exercise says or
what real browsers do, but it's pretty close and avoids changing the
URL parsing too much.

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
    >>> _ = wbemocks.patch_canvas()
    >>> wbemocks.MockCanvas.hide_all()
    >>> import browser

Let's first make sure the bookmarks button is in the right place:

    >>> this_browser = browser.Browser()
    >>> this_browser.chrome.address_rect
    Rect(40, 35, 770, 55)
    >>> this_browser.chrome.bookmarks_rect
    Rect(775, 35, 795, 55)

Note that the address bar needs to be less wide than before, to make
room for the bookmarks bar. 

Let's load a site:

    >>> url_1 = browser.URL(wbemocks.socket.serve("Test"))
    >>> this_browser.new_tab(url_1)

Currently, there should be no bookmarks:

    >>> this_browser.bookmarks
    []
    >>> wbemocks.MockCanvas.all_rects(this_browser.chrome.bookmarks_rect)
    create_rectangle: x1=775 y1=35 x2=795 y2=55 width=1 fill=None

Let's bookmark this site and make sure there's a yellow background:

    >>> this_browser.bookmarks.append(str(url_1))
    >>> this_browser.draw()
    >>> wbemocks.MockCanvas.all_rects(this_browser.chrome.bookmarks_rect)
    create_rectangle: x1=775 y1=35 x2=795 y2=55 width=0 fill='yellow'
    create_rectangle: x1=775 y1=35 x2=795 y2=55 width=1 fill=None

When we click the bookmarks button, we should unbookmark it:

    >>> this_browser.bookmarks
    ['http://test/0']
    >>> rect = this_browser.chrome.bookmarks_rect
    >>> this_browser.handle_click(wbemocks.ClickEvent(rect.left + 1, rect.top + 1))
    >>> wbemocks.MockCanvas.all_rects(this_browser.chrome.bookmarks_rect)
    create_rectangle: x1=775 y1=35 x2=795 y2=55 width=1 fill=None
    >>> this_browser.bookmarks
    []
    >>> this_browser.handle_click(wbemocks.ClickEvent(rect.left + 1, rect.top + 1))
    >>> wbemocks.MockCanvas.all_rects(this_browser.chrome.bookmarks_rect)
    create_rectangle: x1=775 y1=35 x2=795 y2=55 width=0 fill='yellow'
    create_rectangle: x1=775 y1=35 x2=795 y2=55 width=1 fill=None
    >>> this_browser.bookmarks
    ['http://test/0']

Load the second site by typing it in.

    >>> wbemocks.MockCanvas.hide_all()
    >>> url_2 = browser.URL(wbemocks.socket.serve("Another"))
    >>> rect = this_browser.chrome.address_rect
    >>> this_browser.handle_click(wbemocks.ClickEvent(rect.left + 1, rect.top + 1))
    >>> for c in str(url_2):
    ...   this_browser.handle_key(wbemocks.KeyEvent(c))
    >>> this_browser.handle_enter(wbemocks.Event())
    >>> this_browser.tabs[0].url
    URL(scheme=http, host=test, port=80, path='/1')

Load the second site by typing it in again.

    >>> this_browser.handle_click(wbemocks.ClickEvent(50, 51))
    >>> for c in str(url_2):
    ...   this_browser.handle_key(wbemocks.KeyEvent(c))
    >>> this_browser.handle_enter(wbemocks.Event())
    >>> this_browser.tabs[0].url
    URL(scheme=http, host=test, port=80, path='/1')

Make sure it is not bookmarked

    >>> wbemocks.MockCanvas.all_rects(this_browser.chrome.bookmarks_rect)
    create_rectangle: x1=775 y1=35 x2=795 y2=55 width=1 fill=None
    >>> this_browser.bookmarks
    ['http://test/0']

Bookmark it and check.

    >>> this_browser.handle_click(wbemocks.ClickEvent(777, 50))
    >>> wbemocks.MockCanvas.all_rects(this_browser.chrome.bookmarks_rect)
    create_rectangle: x1=775 y1=35 x2=795 y2=55 width=0 fill='yellow'
    create_rectangle: x1=775 y1=35 x2=795 y2=55 width=1 fill=None
    >>> this_browser.bookmarks
    ['http://test/0', 'http://test/1']

Request the bookmark site directly.

    >>> bk_url = browser.URL("about://bookmarks")
    >>> bk_url
    URL(scheme=about, host=None, port=None, path='bookmarks')
    >>> wbemocks.MockCanvas.reset()
    >>> wbemocks.MockCanvas.hide_above(this_browser.chrome.bottom)
    >>> this_browser.new_tab(bk_url)
    create_text: x=13 y=80.25 text=http://test/0 font=Font size=12 weight=normal slant=roman style=None family=Times anchor=nw
    create_text: x=13 y=95.25 text=http://test/1 font=Font size=12 weight=normal slant=roman style=None family=Times anchor=nw
    >>> browser.print_tree(this_browser.active_tab.nodes)
     <html>
       <body>
         <a href="http://test/0">
           'http://test/0'
         <br>
         <a href="http://test/1">
           'http://test/1'
         <br>

Unbookmark the second site.

    >>> wbemocks.MockCanvas.hide_all()
    >>> this_browser.active_tab = this_browser.tabs[0]
    >>> this_browser.draw()
    >>> this_browser.handle_click(wbemocks.ClickEvent(777, 50))
    >>> wbemocks.MockCanvas.all_rects(this_browser.chrome.bookmarks_rect)
    create_rectangle: x1=775 y1=35 x2=795 y2=55 width=1 fill=None
    >>> this_browser.bookmarks
    ['http://test/0']

Request the bookmark site directly.

    >>> bk_url = browser.URL("about://bookmarks")
    >>> bk_url
    URL(scheme=about, host=None, port=None, path='bookmarks')
    >>> this_browser.new_tab(bk_url)
    >>> browser.print_tree(this_browser.active_tab.nodes)
     <html>
       <body>
         <a href="http://test/0">
           'http://test/0'
         <br>

Bookmark the second site again and re-request the bookmarks page:

    >>> this_browser.active_tab = this_browser.tabs[0]
    >>> this_browser.draw()
    >>> this_browser.handle_click(wbemocks.ClickEvent(777, 50))
    >>> wbemocks.MockCanvas.all_rects(this_browser.chrome.bookmarks_rect)
    create_rectangle: x1=775 y1=35 x2=795 y2=55 width=0 fill='yellow'
    create_rectangle: x1=775 y1=35 x2=795 y2=55 width=1 fill=None
    >>> this_browser.bookmarks
    ['http://test/0', 'http://test/1']
    >>> this_browser.new_tab(bk_url)
    >>> browser.print_tree(this_browser.active_tab.nodes)
     <html>
       <body>
         <a href="http://test/0">
           'http://test/0'
         <br>
         <a href="http://test/1">
           'http://test/1'
         <br>
