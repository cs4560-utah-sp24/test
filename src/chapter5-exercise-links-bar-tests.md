Tests for WBE Chapter 5 Exercise `Links Bar`
============================================

    >>> import sys
    >>> sys.path.append("/Users/pavpan/wbe/src/")
    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> _ = test.patch_canvas()
    >>> import browser

The links bar in each chapter is enclosed in `<nav class="links">`.
Importantly, normal `<nav>` elements are *not* the links bar, and
don't have any special styling. Meanwhile, actual links bars should
have a background of `lightgray`.

Let's test that the links bar is displayed correctly by looking at the
HTML tree, layout tree, and display list. First, let's test that
ordinary `<nav>` nodes don't have any special styling. You should be
able to pass with without any changes to the base browser.

    >>> nodes = browser.HTMLParser("""<!doctype html>
    ... <nav>A</nav>B""").parse()
    >>> browser.print_tree(nodes)
     <html>
       <body>
         <nav>
           'A'
         'B'
    >>> doc = browser.DocumentLayout(nodes)
    >>> doc.layout()
    >>> browser.print_tree(doc)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=40.0)
         BlockLayout(x=13, y=18, width=774, height=40.0)
           InlineLayout(x=13, y=18, width=774, height=20.0)
           InlineLayout(x=13, y=38.0, width=774, height=20.0)
    >>> dl = []
    >>> doc.paint(dl)
    >>> dl #doctest: +NORMALIZE_WHITESPACE
    [DrawText(top=21.0 left=13 bottom=37.0 text=A font=Font size=16 weight=normal slant=roman style=None),
     DrawText(top=41.0 left=13 bottom=57.0 text=B font=Font size=16 weight=normal slant=roman style=None)]

Next, let's test that a proper links bar has a `lightgray` background:

    >>> nodes = browser.HTMLParser("""<!doctype html>
    ... <nav class="links">A</nav>B""").parse()
    >>> browser.print_tree(nodes)
     <html>
       <body>
         <nav class="links">
           'A'
         'B'
    >>> doc = browser.DocumentLayout(nodes)
    >>> doc.layout()
    >>> browser.print_tree(doc)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=40.0)
         BlockLayout(x=13, y=18, width=774, height=40.0)
           InlineLayout(x=13, y=18, width=774, height=20.0)
           InlineLayout(x=13, y=38.0, width=774, height=20.0)
    >>> dl = []
    >>> doc.paint(dl)
    >>> dl #doctest: +NORMALIZE_WHITESPACE
    [DrawRect(top=18 left=13 bottom=38.0 right=787 color=lightgray),
     DrawText(top=21.0 left=13 bottom=37.0 text=A font=Font size=16 weight=normal slant=roman style=None),
     DrawText(top=41.0 left=13 bottom=57.0 text=B font=Font size=16 weight=normal slant=roman style=None)]

This should work even if the page has multiple links bars. In this
case, I also write the second links bar `<nav class=links>`, without
the quotes. This should still work because the HTML parser treats both
syntaxes the same.

    >>> nodes = browser.HTMLParser("""<!doctype html>
    ... <nav class="links">A</nav>
    ... B
    ... <nav class=links>C</nav>
    ... """).parse()
    >>> browser.print_tree(nodes)
     <html>
       <body>
         <nav class="links">
           'A'
         '\nB\n'
         <nav class="links">
           'C'
    >>> doc = browser.DocumentLayout(nodes)
    >>> doc.layout()
    >>> browser.print_tree(doc)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=60.0)
         BlockLayout(x=13, y=18, width=774, height=60.0)
           InlineLayout(x=13, y=18, width=774, height=20.0)
           InlineLayout(x=13, y=38.0, width=774, height=20.0)
           InlineLayout(x=13, y=58.0, width=774, height=20.0)
    >>> dl = []
    >>> doc.paint(dl)
    >>> dl #doctest: +NORMALIZE_WHITESPACE
    [DrawRect(top=18 left=13 bottom=38.0 right=787 color=lightgray), 
     DrawText(top=21.0 left=13 bottom=37.0 text=A font=Font size=16 weight=normal slant=roman style=None), 
     DrawText(top=41.0 left=13 bottom=57.0 text=B font=Font size=16 weight=normal slant=roman style=None),
     DrawRect(top=58.0 left=13 bottom=78.0 right=787 color=lightgray), 
     DrawText(top=61.0 left=13 bottom=77.0 text=C font=Font size=16 weight=normal slant=roman style=None)]

Note that both nav bars get a `lightgray` background, and also note
that in both cases the `DrawRect` comes before the `DrawText`, so that
the text appears on top of the background.

Finally, let's test that this works even when there are multiple lines
of text inside the nav bar. This even happens on the book website with
very narrow browsers (like on mobile).

    >>> nodes = browser.HTMLParser("""<!doctype html>
    ... <nav class="links">A<br>C</nav>
    ... B""").parse()
    >>> browser.print_tree(nodes)
     <html>
       <body>
         <nav class="links">
           'A'
           <br>
           'C'
         '\nB'
    >>> doc = browser.DocumentLayout(nodes)
    >>> doc.layout()
    >>> browser.print_tree(doc)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=60.0)
         BlockLayout(x=13, y=18, width=774, height=60.0)
           InlineLayout(x=13, y=18, width=774, height=40.0)
           InlineLayout(x=13, y=58.0, width=774, height=20.0)
    >>> dl = []
    >>> doc.paint(dl)
    >>> dl #doctest: +NORMALIZE_WHITESPACE
    [DrawRect(top=18 left=13 bottom=58.0 right=787 color=lightgray),
     DrawText(top=21.0 left=13 bottom=37.0 text=A font=Font size=16 weight=normal slant=roman style=None),
     DrawText(top=41.0 left=13 bottom=57.0 text=C font=Font size=16 weight=normal slant=roman style=None),
     DrawText(top=61.0 left=13 bottom=77.0 text=B font=Font size=16 weight=normal slant=roman style=None)]
     
Importantly, the background in this case is big enough to contain both lines.
