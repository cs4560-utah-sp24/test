Tests for WBE Chapter 7
=======================

Chapter 7 (Handling Buttons and Links) introduces hit testing, navigation
through link clicks, and browser chrome for the URL bar and tabs.

Tests
=====

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> wbemocks.NORMALIZE_FONT = True
    >>> import browser

    >>> content = """
    ... <div>This is a test<br>Also a test<br>And this too</div>
    ... """
    >>> url = browser.URL(wbemocks.socket.serve(content))
    >>> url
    URL(scheme=http, host=test, port=80, path='/0')

Testing LineLayout and TextLayout
=================================

    >>> this_browser = browser.Browser()
    >>> this_browser.new_tab(url)
    >>> wbemocks.print_list(this_browser.tabs)
    Tab(history=[URL(scheme=http, host=test, port=80, path='/0')])
    >>> browser.print_tree(this_browser.tabs[0].document.node)
     <html>
       <body>
         <div>
           'This is a test'
           <br>
           'Also a test'
           <br>
           'And this too'

Here is how the lines are represented in chapter 7:

    >>> browser.print_tree(this_browser.tabs[0].document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=45.0)
         BlockLayout(x=13, y=18, width=774, height=45.0)
           BlockLayout(x=13, y=18, width=774, height=45.0)
             LineLayout(x=13, y=18, width=774, height=15.0)
               TextLayout(x=13, y=20.25, width=48, height=12, word=This)
               TextLayout(x=73, y=20.25, width=24, height=12, word=is)
               TextLayout(x=109, y=20.25, width=12, height=12, word=a)
               TextLayout(x=133, y=20.25, width=48, height=12, word=test)
             LineLayout(x=13, y=33.0, width=774, height=15.0)
               TextLayout(x=13, y=35.25, width=48, height=12, word=Also)
               TextLayout(x=73, y=35.25, width=12, height=12, word=a)
               TextLayout(x=97, y=35.25, width=48, height=12, word=test)
             LineLayout(x=13, y=48.0, width=774, height=15.0)
               TextLayout(x=13, y=50.25, width=36, height=12, word=And)
               TextLayout(x=61, y=50.25, width=48, height=12, word=this)
               TextLayout(x=121, y=50.25, width=36, height=12, word=too)


Testing Tab
===========

    >>> content = "<a href=\"{}\">Click me</a>".format(url)
    >>> url2 = browser.URL(wbemocks.socket.serve(content))

The browser can have multiple tabs:

    >>> this_browser.new_tab(url2)
    >>> wbemocks.print_list(this_browser.tabs)
    Tab(history=[URL(scheme=http, host=test, port=80, path='/0')])
    Tab(history=[URL(scheme=http, host=test, port=80, path='/1')])

    >>> browser.print_tree(this_browser.tabs[1].document.node)
     <html>
       <body>
         <a href="http://test/0">
           'Click me'

    >>> browser.print_tree(this_browser.tabs[1].document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=15.0)
         BlockLayout(x=13, y=18, width=774, height=15.0)
           LineLayout(x=13, y=18, width=774, height=15.0)
             TextLayout(x=13, y=20.25, width=60, height=12, word=Click)
             TextLayout(x=85, y=20.25, width=24, height=12, word=me)

Tabs supports navigation---clicking on a link to navigate a tab to a new site:

    >>> this_browser.tabs[1].click(14, 21)
    >>> this_browser.tabs[1].url
    URL(scheme=http, host=test, port=80, path='/0')
    >>> browser.print_tree(this_browser.tabs[1].document.node)
     <html>
       <body>
         <div>
           'This is a test'
           <br>
           'Also a test'
           <br>
           'And this too'

The old page is now in the history of the tab:

    >>> this_browser.tabs[1] #doctest: +NORMALIZE_WHITESPACE
    Tab(history=[URL(scheme=http, host=test, port=80, path='/1'), URL(scheme=http, host=test, port=80, path='/0')])

Navigating back restores the old page:

    >>> this_browser.tabs[1].go_back()
    >>> this_browser.tabs[1].url
    URL(scheme=http, host=test, port=80, path='/1')
    >>> browser.print_tree(this_browser.tabs[1].document.node)
     <html>
       <body>
         <a href="http://test/0">
           'Click me'

Clicking on a non-clickable area of the page does nothing:

    >>> this_browser.tabs[1].click(1, 1)
    >>> this_browser.tabs[1].url
    URL(scheme=http, host=test, port=80, path='/1')

Testing Browser
===============

Clicking on a browser tab focuses it:

    >>> this_browser.active_tab
    Tab(history=[URL(scheme=http, host=test, port=80, path='/1')])
    >>> rect = this_browser.chrome.tab_rect(0)
    >>> this_browser.handle_click(wbemocks.Event(rect.left + 1, rect.top + 1))
    >>> this_browser.active_tab
    Tab(history=[URL(scheme=http, host=test, port=80, path='/0')])
    >>> rect = this_browser.chrome.tab_rect(1)
    >>> this_browser.handle_click(wbemocks.Event(rect.left + 1, rect.top + 1))
    >>> this_browser.active_tab
    Tab(history=[URL(scheme=http, host=test, port=80, path='/1')])

Clicking on the address bar focuses it:

    >>> this_browser.handle_click(wbemocks.Event(50, 51))
    >>> this_browser.chrome.focus
    'address bar'

The back button works:

    >>> wbemocks.print_list(this_browser.tabs[1].history)
    URL(scheme=http, host=test, port=80, path='/1')
    >>> this_browser.handle_click(wbemocks.Event(14, this_browser.chrome.bottom + 21))
    >>> wbemocks.print_list(this_browser.tabs[1].history)
    URL(scheme=http, host=test, port=80, path='/1')
    URL(scheme=http, host=test, port=80, path='/0')
    >>> this_browser.handle_click(wbemocks.Event(10, 50))
    >>> wbemocks.print_list(this_browser.tabs[1].history)
    URL(scheme=http, host=test, port=80, path='/1')

Pressing enter with text in the address bar works:

    >>> this_browser.handle_click(wbemocks.Event(50, 51))
    >>> this_browser.chrome.focus
    'address bar'
    >>> this_browser.chrome.address_bar = "http://test/0"
    >>> this_browser.handle_enter(wbemocks.Event(0, 0))
    >>> wbemocks.print_list(this_browser.tabs[1].history)
    URL(scheme=http, host=test, port=80, path='/1')
    URL(scheme=http, host=test, port=80, path='/0')

The home button works:

    >>> content = "Web Browser Engineering homepage"
    >>> browser_engineering = 'https://browser.engineering/'
    >>> wbemocks.socket.respond_ok(browser_engineering, content)
    >>> this_browser.handle_click(wbemocks.Event(10, 10))
    >>> this_browser.tabs #doctest: +NORMALIZE_WHITESPACE
    [Tab(history=[URL(scheme=http, host=test, port=80, path='/0')]),
     Tab(history=[URL(scheme=http, host=test, port=80, path='/1'),
                  URL(scheme=http, host=test, port=80, path='/0')]),
     Tab(history=[URL(scheme=https, host=browser.engineering, port=443, path='/')])]
    
