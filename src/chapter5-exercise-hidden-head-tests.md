Tests for WBE Chapter 5 Exercise `Hidden Head`
=======================

Description
-----------

There’s a good chance your browser is still showing scripts, styles, and page 
  titles at the top of every page you visit. 
Make it so that the `<head>` element and its contents are never displayed. 
Those elements should still be in the HTML tree, but not in the layout tree.

    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> import browser

Set up the URL and web page, this is the content that we will be examining.

    >>> url = 'http://test.test/chapter5_example3'
    >>> content = "<html><head><title>Chapter5</title><script>Don't display me</script></head><body>Do display me</body></html>"
    >>> test.socket.respond_200(url, content)
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
         InlineLayout(x=13, y=18, width=774, height=20.0)
  
The display list should only contain `DrawText` objects for the body text.
  
    >>> this_browser.display_list #doctest: +NORMALIZE_WHITESPACE
     [DrawText(top=21.0 left=13 bottom=37.0 text=Do font=Font size=16 weight=normal slant=roman style=None), 
      DrawText(top=21.0 left=61 bottom=37.0 text=display font=Font size=16 weight=normal slant=roman style=None), 
      DrawText(top=21.0 left=189 bottom=37.0 text=me font=Font size=16 weight=normal slant=roman style=None)]


Make sure the layout tree is not in an invalid state.
The body `BlockLayout` should have no previous sibling.

    >>> print(this_browser.document.children[0].previous)
    None

The parent of the main `BlockLayout` should be the `DocumentLayout`

    >>> this_browser.document.children[0].parent == this_browser.document
    True
    

