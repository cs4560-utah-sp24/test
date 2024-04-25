Tests for WBE Chapter 5 Exercise `Anonymous Block Boxes`
========================================================

Anonymous block boxes: Sometimes, an element has a mix of text-like
and container-like children. For example, in this HTML,

    <div><i>Hello, </i><b>world!</b><p>So it began...</p></div>

the `<div>` element has three children: the `<i>`, `<b>`, and `<p>`
elements. The first two are text-like; the last is container-like.
This is supposed to look like two paragraphs, one for the `<i>` and
`<b>` and the second for the `<p>`. Make your browser do that.
Specifically, modify `BlockLayout` so it can be passed a sequence of
sibling nodes, instead of a single node. Then, modify the algorithm
that constructs the layout tree so that any sequence of text-like
elements gets made into a single `BlockLayout`.

Some quick notes:

- Add an optional `more_nodes` argument to `BlockLayout`. You can
  assume that it will only be used in inline layout mode.
  
- Make sure to process all of the `more_nodes` after processing the
  main `node`.
  
- When creating child `BlockLayout` elements, group runs of text nodes
  and elements not in `BLOCK_ELEMENTS` and make a single `BlockLayout`
  out of each run.

Tests
-----

    >>> import sys
    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> _ = wbemocks.patch_canvas()
    >>> import browser

Let's first test what happens if we have a list of block-level
elements:

    >>> nodes = browser.HTMLParser("""<div>A</div><h6>B</h6><main>C</main>""").parse()
    >>> document = browser.DocumentLayout(nodes)
    >>> document.layout()
    >>> browser.print_tree(document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=45.0, node=<html>)
         BlockLayout(x=13, y=18, width=774, height=45.0, node=<body>)
           BlockLayout(x=13, y=18, width=774, height=15.0, node=<div>)
           BlockLayout(x=13, y=33.0, width=774, height=15.0, node=<h6>)
           BlockLayout(x=13, y=48.0, width=774, height=15.0, node=<main>)

Let's also make sure that this can be painted:

    >>> dl = []
    >>> browser.paint_tree(document, dl)
    >>> wbemocks.print_list(dl)
    DrawText(top=20.25 left=13 bottom=32.25 text=A font=Font size=12 weight=normal slant=roman style=None)
    DrawText(top=35.25 left=13 bottom=47.25 text=B font=Font size=12 weight=normal slant=roman style=None)
    DrawText(top=50.25 left=13 bottom=62.25 text=C font=Font size=12 weight=normal slant=roman style=None)

Next let's test that if you have multiple inline-level elements, that
only creates one `BlockLayout`:

    >>> nodes = browser.HTMLParser("""<i>A</i>B<b>C</b>""").parse()
    >>> document = browser.DocumentLayout(nodes)
    >>> document.layout()
    >>> browser.print_tree(document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=15.0, node=<html>)
         BlockLayout(x=13, y=18, width=774, height=15.0, node=<body>)

That also can be painted:

    >>> dl = []
    >>> browser.paint_tree(document, dl)
    >>> wbemocks.print_list(dl)
    DrawText(top=20.25 left=13 bottom=32.25 text=A font=Font size=12 weight=normal slant=italic style=None)
    DrawText(top=20.25 left=37 bottom=32.25 text=B font=Font size=12 weight=normal slant=roman style=None)
    DrawText(top=20.25 left=61 bottom=32.25 text=C font=Font size=12 weight=bold slant=roman style=None)


Finally, let's test a simple mix of both:

    >>> nodes = browser.HTMLParser("""<div>hi</div><i>A</i>B<b>C</b>""").parse()
    >>> document = browser.DocumentLayout(nodes)
    >>> document.layout()
    >>> browser.print_tree(document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=30.0, node=<html>)
         BlockLayout(x=13, y=18, width=774, height=30.0, node=<body>)
           BlockLayout(x=13, y=18, width=774, height=15.0, node=<div>)
           BlockLayout(x=13, y=33.0, width=774, height=15.0, node=<i>)

That also can be painted:

    >>> dl = []
    >>> browser.paint_tree(document, dl)
    >>> wbemocks.print_list(dl)
    DrawText(top=20.25 left=13 bottom=32.25 text=hi font=Font size=12 weight=normal slant=roman style=None)
    DrawText(top=35.25 left=13 bottom=47.25 text=A font=Font size=12 weight=normal slant=italic style=None)
    DrawText(top=35.25 left=37 bottom=47.25 text=B font=Font size=12 weight=normal slant=roman style=None)
    DrawText(top=35.25 left=61 bottom=47.25 text=C font=Font size=12 weight=bold slant=roman style=None)

One more: let's test it with a complex mix of inline and block:

    >>> content = """hi<div>this</div>is<i>a</i>""" \
    ...     + """<div>test</div><b>of</b> your<div>browser</div> code"""
    >>> nodes = browser.HTMLParser(content).parse()
    >>> document = browser.DocumentLayout(nodes)
    >>> document.layout()
    >>> browser.print_tree(document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=105.0, node=<html>)
         BlockLayout(x=13, y=18, width=774, height=105.0, node=<body>)
           BlockLayout(x=13, y=18, width=774, height=15.0, node='hi')
           BlockLayout(x=13, y=33.0, width=774, height=15.0, node=<div>)
           BlockLayout(x=13, y=48.0, width=774, height=15.0, node='is')
           BlockLayout(x=13, y=63.0, width=774, height=15.0, node=<div>)
           BlockLayout(x=13, y=78.0, width=774, height=15.0, node=<b>)
           BlockLayout(x=13, y=93.0, width=774, height=15.0, node=<div>)
           BlockLayout(x=13, y=108.0, width=774, height=15.0, node=' code')

This, too, can be painted:

    >>> dl = []
    >>> browser.paint_tree(document, dl)
    >>> wbemocks.print_list(dl)
    DrawText(top=20.25 left=13 bottom=32.25 text=hi font=Font size=12 weight=normal slant=roman style=None)
    DrawText(top=35.25 left=13 bottom=47.25 text=this font=Font size=12 weight=normal slant=roman style=None)
    DrawText(top=50.25 left=13 bottom=62.25 text=is font=Font size=12 weight=normal slant=roman style=None)
    DrawText(top=50.25 left=49 bottom=62.25 text=a font=Font size=12 weight=normal slant=italic style=None)
    DrawText(top=65.25 left=13 bottom=77.25 text=test font=Font size=12 weight=normal slant=roman style=None)
    DrawText(top=80.25 left=13 bottom=92.25 text=of font=Font size=12 weight=bold slant=roman style=None)
    DrawText(top=80.25 left=49 bottom=92.25 text=your font=Font size=12 weight=normal slant=roman style=None)
    DrawText(top=95.25 left=13 bottom=107.25 text=browser font=Font size=12 weight=normal slant=roman style=None)
    DrawText(top=110.25 left=13 bottom=122.25 text=code font=Font size=12 weight=normal slant=roman style=None)
