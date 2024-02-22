Tests for WBE Chapter 7 Exercise `Middle Click`
===============================================

Add support for middle-clicking on a link (`Button-2`) to open it in a
new tab. You might need a mouse to test this easily.

Name the method in the `Browser` class that handles the middle click event
`handle_middle_click`. The new tabs should be opened in the background

Test code
---------

Boilerplate.

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> import browser

First we need to set up two pages, where one is a link to the other.
This is the page linked _to_.

    >>> body_dst = 'Link destination'
    >>> url_dst = browser.URL(wbemocks.socket.serve(body_dst))

This is the page with the link to the above destination.

    >>> body_src = f'<a href="{url_dst}">Click here</a>'
    >>> url_src = browser.URL(wbemocks.socket.serve(body_src))

Load up the source site in the browser.
There will be one tab open with the source url which is the selected tab.

    >>> this_browser = browser.Browser()
    >>> this_browser.new_tab(url_src)
    >>> len(this_browser.tabs)
    1
    >>> this_browser.tabs[0].url
    URL(scheme=http, host=test, port=80, path='/1')
    >>> this_browser.active_tab
    Tab(history=[URL(scheme=http, host=test, port=80, path='/1')])
    >>> this_browser.chrome.focus == None
    True

Clicking on the link using a middle click should keep the current tab, and open
  a new one with the destination site.
The active tab should still be the one with the source url.

    >>> this_browser.handle_middle_click(wbemocks.ClickEvent(14, this_browser.chrome.bottom + 21))
    >>> len(this_browser.tabs)
    2
    >>> this_browser.tabs[0].url
    URL(scheme=http, host=test, port=80, path='/1')
    >>> this_browser.tabs[1].url
    URL(scheme=http, host=test, port=80, path='/0')
    >>> this_browser.active_tab
    Tab(history=[URL(scheme=http, host=test, port=80, path='/1')])
    >>> this_browser.chrome.focus == None
    True

Using middle click anywhere that is not a link should not change anything.

    >>> this_browser.handle_middle_click(wbemocks.ClickEvent(1, 1))
    >>> len(this_browser.tabs)
    2
    >>> this_browser.tabs[0].url
    URL(scheme=http, host=test, port=80, path='/1')
    >>> this_browser.tabs[1].url
    URL(scheme=http, host=test, port=80, path='/0')
    >>> this_browser.active_tab
    Tab(history=[URL(scheme=http, host=test, port=80, path='/1')])
    >>> this_browser.chrome.focus == None
    True


Middle click on the address bar.

    >>> this_browser.handle_middle_click(wbemocks.ClickEvent(50, 41))
    >>> len(this_browser.tabs)
    2
    >>> this_browser.tabs[0].url
    URL(scheme=http, host=test, port=80, path='/1')
    >>> this_browser.tabs[1].url
    URL(scheme=http, host=test, port=80, path='/0')
    >>> this_browser.active_tab
    Tab(history=[URL(scheme=http, host=test, port=80, path='/1')])
    >>> this_browser.chrome.focus == None
    True

Middle click on the one-th tab.

    >>> this_browser.handle_middle_click(wbemocks.ClickEvent(120, 1))
    >>> len(this_browser.tabs)
    2
    >>> this_browser.tabs[0].url
    URL(scheme=http, host=test, port=80, path='/1')
    >>> this_browser.tabs[1].url
    URL(scheme=http, host=test, port=80, path='/0')
    >>> this_browser.active_tab
    Tab(history=[URL(scheme=http, host=test, port=80, path='/1')])
    >>> this_browser.chrome.focus == None
    True

Middle click on the new tab button.

    >>> this_browser.handle_middle_click(wbemocks.ClickEvent(20, 20))
    >>> len(this_browser.tabs)
    2
    >>> this_browser.tabs[0].url
    URL(scheme=http, host=test, port=80, path='/1')
    >>> this_browser.tabs[1].url
    URL(scheme=http, host=test, port=80, path='/0')
    >>> this_browser.active_tab
    Tab(history=[URL(scheme=http, host=test, port=80, path='/1')])
    >>> this_browser.chrome.focus == None
    True
