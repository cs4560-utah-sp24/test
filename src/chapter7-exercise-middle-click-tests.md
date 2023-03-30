Tests for WBE Chapter 7 Exercise `Middle Click`
===============================================

Description
-----------

Add support for middle-clicking on a link (Button-2) to open it in a new tab.
You might need a mouse to test this easily.


Extra Requirements
------------------

* Name the method in the `Browser` class that handles the middle click event
  `handle_middle_click`
* The new tabs should be opened in the background


Test code
---------

Boilerplate.

    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> import browser

First we need to set up two pages, where one is a link to the other.
This is the page linked _to_.

    >>> url_dst = 'http://test.test/chapter7-link-dst'
    >>> body_dst = 'Link destination'
    >>> test.socket.respond_200(url_dst, body_dst)

This is the page with the link to the above destination.

    >>> url_src = 'http://test.test/chapter7-link-src'
    >>> body_src = f'<a href="{url_dst}">Click here</a>'
    >>> test.socket.respond_200(url_src, body_src)

Load up the source site in the browser.
There will be one tab open with the source url which is the selected tab.

    >>> this_browser = browser.Browser()
    >>> this_browser.load(url_src)
    >>> len(this_browser.tabs)
    1
    >>> this_browser.tabs[0].url
    'http://test.test/chapter7-link-src'
    >>> this_browser.active_tab
    0
    >>> this_browser.focus == None
    True

Clicking on the link using a middle click should keep the current tab, and open
  a new one with the destination site.
The active tab should still be the one with the source url.

    >>> this_browser.handle_middle_click(test.Event(14, 121))
    >>> len(this_browser.tabs)
    2
    >>> this_browser.tabs[0].url
    'http://test.test/chapter7-link-src'
    >>> this_browser.tabs[1].url
    'http://test.test/chapter7-link-dst'
    >>> this_browser.active_tab
    0
    >>> this_browser.focus == None
    True

Using middle click anywhere that is not a link should not change anything.
Middle click somewhere that has nothing there.

    >>> this_browser.handle_middle_click(test.Event(1, 1))
    >>> len(this_browser.tabs)
    2
    >>> this_browser.tabs[0].url
    'http://test.test/chapter7-link-src'
    >>> this_browser.tabs[1].url
    'http://test.test/chapter7-link-dst'
    >>> this_browser.active_tab
    0
    >>> this_browser.focus == None
    True


Middle click on the address bar.

    >>> this_browser.handle_middle_click(test.Event(50, 41))
    >>> len(this_browser.tabs)
    2
    >>> this_browser.tabs[0].url
    'http://test.test/chapter7-link-src'
    >>> this_browser.tabs[1].url
    'http://test.test/chapter7-link-dst'
    >>> this_browser.active_tab
    0
    >>> this_browser.focus == None
    True

Middle click on the one-th tab.

    >>> this_browser.handle_middle_click(test.Event(120, 1))
    >>> len(this_browser.tabs)
    2
    >>> this_browser.tabs[0].url
    'http://test.test/chapter7-link-src'
    >>> this_browser.tabs[1].url
    'http://test.test/chapter7-link-dst'
    >>> this_browser.active_tab
    0
    >>> this_browser.focus == None
    True

Middle click on the new tab button.

    >>> this_browser.handle_middle_click(test.Event(20, 20))
    >>> len(this_browser.tabs)
    2
    >>> this_browser.tabs[0].url
    'http://test.test/chapter7-link-src'
    >>> this_browser.tabs[1].url
    'http://test.test/chapter7-link-dst'
    >>> this_browser.active_tab
    0
    >>> this_browser.focus == None
    True
