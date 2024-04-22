Tests for WBE Chapter 6 Exercise `Width/Height`
=======================

Add support to block layout objects for the width and height
properties. These can either be a pixel value, which directly sets the
width or height of the layout object, or the word `auto`, in which
case the existing layout algorithm is used.

If for some reason a negative width or height is specified, that
should also be interpreted as if `auto` was used. (Technically, in
CSS, this should be a syntax error, which would cause the whole
`width` property to be ignored, but we're implementing different
behavior here to make it easier.)

Tests
-----

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> import browser

With no width or height properties the browser should perform the existing layout.

    >>> body = "<div>Auto layout</div>"
    >>> url = browser.URL(wbemocks.socket.serve(body))
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    >>> browser.print_tree(this_browser.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=15.0, node=<html>)
         BlockLayout(x=13, y=18, width=774, height=15.0, node=<body>)
           BlockLayout(x=13, y=18, width=774, height=15.0, node=<div>)

Specifying width should set the width of the element.

    >>> body = '<div style="width:1000px">Set width</div>'
    >>> url = browser.URL(wbemocks.socket.serve(body))
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    >>> browser.print_tree(this_browser.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=15.0, node=<html>)
         BlockLayout(x=13, y=18, width=774, height=15.0, node=<body>)
           BlockLayout(x=13, y=18, width=1000.0, height=15.0, node=<div style="width:1000px">)

Specifying height changes the element's hight, which will in turn cascade up the tree.

    >>> body = '<div style="height:100px">Set height</div>'
    >>> url = browser.URL(wbemocks.socket.serve(body))
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    >>> browser.print_tree(this_browser.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=100.0, node=<html>)
         BlockLayout(x=13, y=18, width=774, height=100.0, node=<body>)
           BlockLayout(x=13, y=18, width=774, height=100.0, node=<div style="height:100px">)

You should be able to set both simultaneously.

    >>> body = '<div style="width:900px;height:200px">Set both</div>'
    >>> url = browser.URL(wbemocks.socket.serve(body))
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    >>> browser.print_tree(this_browser.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=200.0, node=<html>)
         BlockLayout(x=13, y=18, width=774, height=200.0, node=<body>)
           BlockLayout(x=13, y=18, width=900.0, height=200.0, node=<div style="width:900px;height:200px">)

If a value is negative you should use the automatic layout.

    >>> body = '<div style="width:-10px">Default to auto</div>'
    >>> url = browser.URL(wbemocks.socket.serve(body))
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    >>> browser.print_tree(this_browser.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=15.0, node=<html>)
         BlockLayout(x=13, y=18, width=774, height=15.0, node=<body>)
           BlockLayout(x=13, y=18, width=774, height=15.0, node=<div style="width:-10px">)

Make sure that text wrapping still works.
In this example the height of the `div` is due to text wrapping.

    >>> body = '<div style="width:100px">Wrap me since width is set</div>'
    >>> url = browser.URL(wbemocks.socket.serve(body))
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    >>> browser.print_tree(this_browser.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=60.0, node=<html>)
         BlockLayout(x=13, y=18, width=774, height=60.0, node=<body>)
           BlockLayout(x=13, y=18, width=100.0, height=60.0, node=<div style="width:100px">)


    >>> body = '<div style="height:150px"><p>foo</p></div>'
    >>> url = browser.URL(wbemocks.socket.serve(body))
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    >>> browser.print_tree(this_browser.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=150.0, node=<html>)
         BlockLayout(x=13, y=18, width=774, height=150.0, node=<body>)
           BlockLayout(x=13, y=18, width=774, height=150.0, node=<div style="height:150px">)
             BlockLayout(x=13, y=18, width=774, height=15.0, node=<p>)
