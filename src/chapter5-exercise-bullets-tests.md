Tests for WBE Chapter 5 Exercise `Bullets`
=======================

Description
-----------

Add bullets to list items, which in HTML are `<li>` tags. 
You can make them little squares, located to the left of the list item itself. 
Also indent `<li>` elements so the text inside the element is to the right of 
  the bullet point.


    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> import browser

Set up the URL and web page, this is the content that we will be examining.

    >>> url = 'http://test.test/chapter5_example4'
    >>> content = "<html><body><li>hello</li><li>world</li></body></html>"
    >>> test.socket.respond_200(url, content)
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)

The layout tree should only contain two inline layout objects, corresponding to
  the body of the web page.
         
    >>> browser.print_tree(this_browser.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=40.0)
         BlockLayout(x=13, y=18, width=774, height=40.0)
           InlineLayout(x=39, y=18, width=748, height=20.0)
           InlineLayout(x=39, y=38.0, width=748, height=20.0)

The text inside the `li` should be indented over by `2 * HSTEP`.
The bullet itself should be a black rectangle, 4 by 4 pixels, centered 
  vertically on the line and with a horizontal center one `HSTEP` from the 
  start of the line.
The `DrawRect` call should in the `paint` function's output display list before
  the text of the `li`.
  
    >>> this_browser.display_list #doctest: +NORMALIZE_WHITESPACE
    [DrawRect(top=26.0 left=24 bottom=30.0 right=28 color=black), 
     DrawText(top=21.0 left=39 bottom=37.0 text=hello font=Font size=16 weight=normal slant=roman style=None), 
     DrawRect(top=46.0 left=24 bottom=50.0 right=28 color=black), 
     DrawText(top=41.0 left=39 bottom=57.0 text=world font=Font size=16 weight=normal slant=roman style=None)]

It is possible that multiple lines are contained in a `li`, and in these
  cases all lines should be indented and the bullet should be vertically 
  centered on the first line.

    >>> url = 'http://test.test/chapter5_example5'
    >>> content = "<html><body><li>hello<br>world</li></body></html>"
    >>> test.socket.respond_200(url, content)
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    >>> this_browser.display_list #doctest: +NORMALIZE_WHITESPACE
    [DrawRect(top=26.0 left=24 bottom=30.0 right=28 color=black), 
     DrawText(top=21.0 left=39 bottom=37.0 text=hello font=Font size=16 weight=normal slant=roman style=None), 
     DrawText(top=41.0 left=39 bottom=57.0 text=world font=Font size=16 weight=normal slant=roman style=None)]
