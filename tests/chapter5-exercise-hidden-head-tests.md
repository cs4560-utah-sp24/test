Tests for WBE Chapter 5 Exercise `Hidden Head`
=======================

There’s a good chance your browser is still showing scripts, styles,
and page titles at the top of every page you visit. Make it so that
the `<head>` element and its contents are never displayed. Those
elements should still be in the HTML tree, but not in the layout tree.

Tests
-----

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> import browser

Set up the URL and web page, this is the content that we will be examining.

    >>> content = "<html><head><title>Chapter5</title><script>Don't display me</script></head><body>Do display me</body></html>"
    >>> url = browser.URL(wbemocks.socket.serve(content))
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)

The HMTL tree should contain the `<head>` elements

    >>> browser.print_tree(this_browser.nodes)
     <html>
       <head>
         <title>
           'Chapter5'
         <script>
           "Don't display me"
       <body>
         'Do display me'

The layout tree should only contain one inline layout object, corresponding to
  the body of the web page.
         
    >>> browser.print_tree(this_browser.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=20.0)
         BlockLayout(x=13, y=18, width=774, height=20.0)
  
The display list should only contain `DrawText` objects for the body text.
  
    >>> wbemocks.print_list(this_browser.display_list)
    DrawText(top=21.0 left=13 bottom=37.0 text=Do font=Font size=16 weight=normal slant=roman style=None)
    DrawText(top=21.0 left=61 bottom=37.0 text=display font=Font size=16 weight=normal slant=roman style=None)
    DrawText(top=21.0 left=189 bottom=37.0 text=me font=Font size=16 weight=normal slant=roman style=None)


Make sure the layout tree is not in an invalid state.
The body `BlockLayout` should have no previous sibling.

    >>> print(this_browser.document.children[0].previous)
    None

The parent of the main `BlockLayout` should be the `DocumentLayout`

    >>> this_browser.document.children[0].parent == this_browser.document
    True
    

