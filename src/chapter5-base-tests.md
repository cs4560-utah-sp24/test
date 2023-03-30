Tests for WBE Chapter 5
=======================

Chapter 5 (Laying Out Pages) introduces inline and block layout modes on
the document tree, and introduces the concept of the document tree, and
adds support for drawing the background colors of document tree elements.

    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> import browser

Testing layout_mode
===================

The `layout_mode` function returns "inline" if the object is a `Text` node
or has all inline children, and otherwise returns "block".

    >>> parser = browser.HTMLParser("text")
    >>> document_tree = parser.parse()
    >>> browser.print_tree(document_tree)
     <html>
       <body>
         'text'
    >>> browser.layout_mode(document_tree)
    'block'
    >>> browser.layout_mode(document_tree.children[0])
    'inline'
    
Here's some tests on a bigger, more complex document

    >>> sample_html = "<div></div><div>text</div><div><div></div>text</div><span></span><span>text</span>"
    >>> parser = browser.HTMLParser(sample_html)
    >>> document_tree = parser.parse()
    >>> browser.print_tree(document_tree)
     <html>
       <body>
         <div>
         <div>
           'text'
         <div>
           <div>
           'text'
         <span>
         <span>
           'text'

The body element has block layout mode, because it has two block-element children.

    >>> browser.layout_mode(document_tree.children[0])
    'block'

The first div has block layout mode, because it has no children.

    >>> browser.layout_mode(document_tree.children[0].children[0])
    'block'

The second div has inline layout mode, because it has one text child.

    >>> browser.layout_mode(document_tree.children[0].children[1])
    'inline'

The third div has block layout mode, because it has one block and one inline child.

    >>> browser.layout_mode(document_tree.children[0].children[2])
    'block'

The first span has block layout mode, even though spans are inline normally:

    >>> browser.layout_mode(document_tree.children[0].children[3])
    'block'

The span has block layout mode, even though spans are inline normally:

    >>> browser.layout_mode(document_tree.children[0].children[4])
    'inline'

Testing the layout tree
=======================

    >>> url = 'http://test.test/chapter5_example1'
    >>> test.socket.respond_200(url, sample_html)
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    >>> browser.print_tree(this_browser.nodes)
     <html>
       <body>
         <div>
         <div>
           'text'
         <div>
           <div>
           'text'
         <span>
         <span>
           'text'

    >>> browser.print_tree(this_browser.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=60.0)
         BlockLayout(x=13, y=18, width=774, height=60.0)
           BlockLayout(x=13, y=18, width=774, height=0)
           InlineLayout(x=13, y=18, width=774, height=20.0)
           BlockLayout(x=13, y=38.0, width=774, height=20.0)
             BlockLayout(x=13, y=38.0, width=774, height=0)
             InlineLayout(x=13, y=38.0, width=774, height=20.0)
           BlockLayout(x=13, y=58.0, width=774, height=0)
           InlineLayout(x=13, y=58.0, width=774, height=20.0)

    >>> this_browser.display_list #doctest: +NORMALIZE_WHITESPACE
    [DrawText(top=21.0 left=13 bottom=37.0 text=text font=Font size=16 weight=normal slant=roman style=None), 
     DrawText(top=41.0 left=13 bottom=57.0 text=text font=Font size=16 weight=normal slant=roman style=None), 
     DrawText(top=61.0 left=13 bottom=77.0 text=text font=Font size=16 weight=normal slant=roman style=None)]

Testing background painting
===========================

`<pre>` elements have a gray background.

    >>> url = 'http://test.test/chapter5_example2'
    >>> test.socket.respond_200(url, "<pre>pre text</pre>")
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    >>> browser.print_tree(this_browser.nodes)
     <html>
       <body>
         <pre>
           'pre text'

    >>> browser.print_tree(this_browser.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=20.0)
         BlockLayout(x=13, y=18, width=774, height=20.0)
           InlineLayout(x=13, y=18, width=774, height=20.0)

The first display list entry is now a gray rect, since it's for a `<pre>` element:

    >>> this_browser.display_list[0]
    DrawRect(top=18 left=13 bottom=38.0 right=787 color=gray)
