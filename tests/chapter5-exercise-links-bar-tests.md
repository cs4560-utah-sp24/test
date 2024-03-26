Tests for WBE Chapter 5 Exercise `Links Bar`
============================================

At the top and bottom of each chapter of this book is a gray bar
naming the chapter and offering back and forward links. It is enclosed
in a `<nav class="links">` tag. Have your browser give this links bar
the light gray background a real browser would.

Give links bars a background of `lightgray`. Normal `<nav>` elements
are *not* the links bar, and don't have any special styling.

Tests
-----

    >>> import sys
    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> _ = wbemocks.patch_canvas()
    >>> import browser

The links bar in each chapter is enclosed in `<nav class="links">`.

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
           BlockLayout(x=13, y=18, width=774, height=20.0)
           BlockLayout(x=13, y=38.0, width=774, height=20.0)
    >>> dl = []
    >>> browser.paint_tree(doc, dl)
    >>> wbemocks.print_list(dl)
    DrawText(top=21.0 left=13 bottom=37.0 text=A font=Font size=16 weight=normal slant=roman style=None)
    DrawText(top=41.0 left=13 bottom=57.0 text=B font=Font size=16 weight=normal slant=roman style=None)

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
           BlockLayout(x=13, y=18, width=774, height=20.0)
           BlockLayout(x=13, y=38.0, width=774, height=20.0)
    >>> dl = []
    >>> browser. (doc, dl)
    >>> wbemocks.print_list(dl)
    DrawRect(top=18 left=13 bottom=38.0 right=787 color=lightgray)
    DrawText(top=21.0 left=13 bottom=37.0 text=A font=Font size=16 weight=normal slant=roman style=None)
    DrawText(top=41.0 left=13 bottom=57.0 text=B font=Font size=16 weight=normal slant=roman style=None)

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
           BlockLayout(x=13, y=18, width=774, height=20.0)
           BlockLayout(x=13, y=38.0, width=774, height=20.0)
           BlockLayout(x=13, y=58.0, width=774, height=20.0)
    >>> dl = []
    >>> browser.paint_tree(doc, dl)
    >>> wbemocks.print_list(dl)
    DrawRect(top=18 left=13 bottom=38.0 right=787 color=lightgray)
    DrawText(top=21.0 left=13 bottom=37.0 text=A font=Font size=16 weight=normal slant=roman style=None)
    DrawText(top=41.0 left=13 bottom=57.0 text=B font=Font size=16 weight=normal slant=roman style=None)
    DrawRect(top=58.0 left=13 bottom=78.0 right=787 color=lightgray)
    DrawText(top=61.0 left=13 bottom=77.0 text=C font=Font size=16 weight=normal slant=roman style=None)

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
           BlockLayout(x=13, y=18, width=774, height=40.0)
           BlockLayout(x=13, y=58.0, width=774, height=20.0)
    >>> dl = []
    >>> browser.paint_tree(doc, dl)
    >>> wbemocks.print_list(dl)
    DrawRect(top=18 left=13 bottom=58.0 right=787 color=lightgray)
    DrawText(top=21.0 left=13 bottom=37.0 text=A font=Font size=16 weight=normal slant=roman style=None)
    DrawText(top=41.0 left=13 bottom=57.0 text=C font=Font size=16 weight=normal slant=roman style=None)
    DrawText(top=61.0 left=13 bottom=77.0 text=B font=Font size=16 weight=normal slant=roman style=None)
     
Importantly, the background in this case is big enough to contain both lines.

Ensure `<nav>` elements without a class attribute correctly split multiple words and do not display any special background styling.

    >>> nodes = browser.HTMLParser("""<!doctype html>
    ... <nav>Word1 Word2 Word3</nav>B""").parse()
    >>> browser.print_tree(nodes)
     <html>
       <body>
         <nav>
           'Word1 Word2 Word3'
         'B'

    >>> doc = browser.DocumentLayout(nodes)
    >>> doc.layout()
    >>> browser.print_tree(doc)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=40.0)
         BlockLayout(x=13, y=18, width=774, height=40.0)
           BlockLayout(x=13, y=18, width=774, height=20.0)
           BlockLayout(x=13, y=38.0, width=774, height=20.0)

    >>> dl = []
    >>> browser.paint_tree(doc, dl)
    >>> wbemocks.print_list(dl)
    DrawText(top=21.0 left=13 bottom=37.0 text=Word1 font=Font size=16 weight=normal slant=roman style=None)
    DrawText(top=21.0 left=109 bottom=37.0 text=Word2 font=Font size=16 weight=normal slant=roman style=None)
    DrawText(top=21.0 left=205 bottom=37.0 text=Word3 font=Font size=16 weight=normal slant=roman style=None)
    DrawText(top=41.0 left=13 bottom=57.0 text=B font=Font size=16 weight=normal slant=roman style=None)


Make sure your browser treats the class attribute in HTML case-insensitively, recognizing class names regardless of letter case.

    >>> nodes = browser.HTMLParser("""<!doctype html>
    ... <nav class="LINKS">A</nav>B""").parse()
    >>> browser.print_tree(nodes)
     <html>
       <body>
         <nav class="LINKS">
           'A'
         'B'

    >>> doc = browser.DocumentLayout(nodes)
    >>> doc.layout()
    >>> browser.print_tree(doc)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=40.0)
         BlockLayout(x=13, y=18, width=774, height=40.0)
           BlockLayout(x=13, y=18, width=774, height=20.0)
           BlockLayout(x=13, y=38.0, width=774, height=20.0)

    >>> dl = []
    >>> browser.paint_tree(doc, dl)
    >>> wbemocks.print_list(dl)
    DrawRect(top=18 left=13 bottom=38.0 right=787 color=lightgray)
    DrawText(top=21.0 left=13 bottom=37.0 text=A font=Font size=16 weight=normal slant=roman style=None)
    DrawText(top=41.0 left=13 bottom=57.0 text=B font=Font size=16 weight=normal slant=roman style=None)