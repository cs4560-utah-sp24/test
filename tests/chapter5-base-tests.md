Tests for WBE Chapter 5
=======================

Chapter 5 (Laying Out Pages) introduces inline and block layout modes on
the document tree, and introduces the concept of the document tree, and
adds support for drawing the background colors of document tree elements.

To pass the tests, you'll need to add `__repr__` methods to the new
layout classes:

```
class BlockLayout:
    def __repr__(self):
        return "BlockLayout(x={}, y={}, width={}, height={})".format(
            self.x, self.y, self.width, self.height)

class DocumentLayout:
    def __repr__(self):
        return "DocumentLayout()"
```

You'll also need `__repr__` methods for drawing commands:

```
class DrawText:
    def __repr__(self):
        return "DrawText(top={} left={} bottom={} text={} font={})" \
            .format(self.top, self.left, self.bottom, self.text, self.font)

class DrawRect:
    def __repr__(self):
        return "DrawRect(top={} left={} bottom={} right={} color={})".format(
            self.top, self.left, self.bottom, self.right, self.color)
```


Testing layout_mode
===================

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> import browser

The `layout_mode` function returns "inline" if the object is a `Text` node
or has all inline children, and otherwise returns "block".

    >>> html = "text"
    >>> document_tree = browser.HTMLParser(html).parse()
    >>> browser.print_tree(document_tree)
     <html>
       <body>
         'text'
    >>> lmode = lambda n: browser.BlockLayout(n, None, None).layout_mode()
    >>> lmode(document_tree)
    'block'
    >>> lmode(document_tree.children[0])
    'inline'
    
Here's some tests on a bigger, more complex document

    >>> html = "<div></div><div>text</div><div><div></div>text</div><span>text</span>"
    >>> document_tree = browser.HTMLParser(html).parse()
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
           'text'

The body element has block layout mode, because it has two block-element children.

    >>> lmode(document_tree.children[0])
    'block'

The first div has block layout mode, because it has no children.

    >>> lmode(document_tree.children[0].children[0])
    'block'

The second div has inline layout mode, because it has one text child.

    >>> lmode(document_tree.children[0].children[1])
    'inline'

The third div has block layout mode, because it has one block and one inline child.

    >>> lmode(document_tree.children[0].children[2])
    'block'

The span has inline layout mode, because spans are inline normally:

    >>> lmode(document_tree.children[0].children[3])
    'inline'

Testing the layout tree
=======================

    >>> url = browser.URL(wbemocks.socket.serve(html))
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
           'text'

    >>> browser.print_tree(this_browser.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=60.0)
         BlockLayout(x=13, y=18, width=774, height=60.0)
           BlockLayout(x=13, y=18, width=774, height=0)
           BlockLayout(x=13, y=18, width=774, height=20.0)
           BlockLayout(x=13, y=38.0, width=774, height=20.0)
             BlockLayout(x=13, y=38.0, width=774, height=0)
             BlockLayout(x=13, y=38.0, width=774, height=20.0)
           BlockLayout(x=13, y=58.0, width=774, height=20.0)

    >>> this_browser.display_list #doctest: +NORMALIZE_WHITESPACE
    [DrawText(top=21.0 left=13 bottom=37.0 text=text font=Font size=16 weight=normal slant=roman style=None), 
     DrawText(top=41.0 left=13 bottom=57.0 text=text font=Font size=16 weight=normal slant=roman style=None), 
     DrawText(top=61.0 left=13 bottom=77.0 text=text font=Font size=16 weight=normal slant=roman style=None)]

Testing background painting
===========================

`<pre>` elements have a gray background.

    >>> html = "<pre>pre text</pre>"
    >>> url = browser.URL(wbemocks.socket.serve(html))
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
           BlockLayout(x=13, y=18, width=774, height=20.0)

The first display list entry is now a gray rect, since it's for a `<pre>` element:

    >>> this_browser.display_list[0]
    DrawRect(top=18 left=13 bottom=38.0 right=787 color=gray)
