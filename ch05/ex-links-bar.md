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
    >>> wbemocks.MockCanvas.hide_all()
    >>> import browser

The links bar in each chapter is enclosed in `<nav class="links">`.

Let's test that the links bar is displayed correctly by looking at the
HTML tree, layout tree, and display list. First, let's test that
ordinary `<nav>` nodes don't have any special styling. You should be
able to pass with without any changes to the base browser.

    >>> url = wbemocks.socket.serve("""<!doctype html>
    ... <nav>A</nav>B""")
    >>> this_browser = browser.Browser()
    >>> this_browser.load(browser.URL(url))
    >>> browser.print_tree(this_browser.nodes)
     <html>
       <body>
         <nav>
           'A'
         'B'

    >>> browser.print_tree(this_browser.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=30.0, node=<html>)
         BlockLayout(x=13, y=18, width=774, height=30.0, node=<body>)
           BlockLayout(x=13, y=18, width=774, height=15.0, node=<nav>)
           BlockLayout(x=13, y=33.0, width=774, height=15.0, node='B')
    >>> wbemocks.print_list(this_browser.display_list)
    DrawText(top=20.25 left=13 bottom=32.25 text=A font=Font size=12 weight=normal slant=roman style=None)
    DrawText(top=35.25 left=13 bottom=47.25 text=B font=Font size=12 weight=normal slant=roman style=None)

Next, let's test that a proper links bar has a `lightgray` background:

    >>> url = wbemocks.socket.serve("""<!doctype html>
    ... <nav class="links">A</nav>B""")
    >>> this_browser = browser.Browser()
    >>> this_browser.load(browser.URL(url))
    >>> browser.print_tree(this_browser.nodes)
     <html>
       <body>
         <nav class="links">
           'A'
         'B'

    >>> browser.print_tree(this_browser.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=30.0, node=<html>)
         BlockLayout(x=13, y=18, width=774, height=30.0, node=<body>)
           BlockLayout(x=13, y=18, width=774, height=15.0, node=<nav class="links">)
           BlockLayout(x=13, y=33.0, width=774, height=15.0, node='B')

    >>> wbemocks.print_list(this_browser.display_list)
    DrawRect(top=18 left=13 bottom=33.0 right=787 color=lightgray)
    DrawText(top=20.25 left=13 bottom=32.25 text=A font=Font size=12 weight=normal slant=roman style=None)
    DrawText(top=35.25 left=13 bottom=47.25 text=B font=Font size=12 weight=normal slant=roman style=None)

This should work even if the page has multiple links bars. In this
case, I also write the second links bar `<nav class=links>`, without
the quotes. This should still work because the HTML parser treats both
syntaxes the same.

    >>> url = wbemocks.socket.serve("""<!doctype html>
    ... <nav class="links">A</nav>
    ... B
    ... <nav class=links>C</nav>
    ... """)
    >>> this_browser = browser.Browser()
    >>> this_browser.load(browser.URL(url))
    >>> browser.print_tree(this_browser.nodes)
     <html>
       <body>
         <nav class="links">
           'A'
         '\nB\n'
         <nav class="links">
           'C'

    >>> browser.print_tree(this_browser.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=45.0, node=<html>)
         BlockLayout(x=13, y=18, width=774, height=45.0, node=<body>)
           BlockLayout(x=13, y=18, width=774, height=15.0, node=<nav class="links">)
           BlockLayout(x=13, y=33.0, width=774, height=15.0, node='\nB\n')
           BlockLayout(x=13, y=48.0, width=774, height=15.0, node=<nav class="links">)

    >>> wbemocks.print_list(this_browser.display_list)
    DrawRect(top=18 left=13 bottom=33.0 right=787 color=lightgray)
    DrawText(top=20.25 left=13 bottom=32.25 text=A font=Font size=12 weight=normal slant=roman style=None)
    DrawText(top=35.25 left=13 bottom=47.25 text=B font=Font size=12 weight=normal slant=roman style=None)
    DrawRect(top=48.0 left=13 bottom=63.0 right=787 color=lightgray)
    DrawText(top=50.25 left=13 bottom=62.25 text=C font=Font size=12 weight=normal slant=roman style=None)

Note that both nav bars get a `lightgray` background, and also note
that in both cases the `DrawRect` comes before the `DrawText`, so that
the text appears on top of the background.

Finally, let's test that this works even when there are multiple lines
of text inside the nav bar. This even happens on the book website with
very narrow browsers (like on mobile).

    >>> url = wbemocks.socket.serve("""<!doctype html>
    ... <nav class="links">A<br>C</nav>
    ... B""")
    >>> this_browser = browser.Browser()
    >>> this_browser.load(browser.URL(url))
    >>> browser.print_tree(this_browser.nodes)
     <html>
       <body>
         <nav class="links">
           'A'
           <br>
           'C'
         '\nB'
    >>> browser.print_tree(this_browser.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=45.0, node=<html>)
         BlockLayout(x=13, y=18, width=774, height=45.0, node=<body>)
           BlockLayout(x=13, y=18, width=774, height=30.0, node=<nav class="links">)
           BlockLayout(x=13, y=48.0, width=774, height=15.0, node='\nB')
    >>> wbemocks.print_list(this_browser.display_list)
    DrawRect(top=18 left=13 bottom=48.0 right=787 color=lightgray)
    DrawText(top=20.25 left=13 bottom=32.25 text=A font=Font size=12 weight=normal slant=roman style=None)
    DrawText(top=35.25 left=13 bottom=47.25 text=C font=Font size=12 weight=normal slant=roman style=None)
    DrawText(top=50.25 left=13 bottom=62.25 text=B font=Font size=12 weight=normal slant=roman style=None)
     
Importantly, the background in this case is big enough to contain both lines.

Ensure `<nav>` elements without a class attribute correctly split multiple words and do not display any special background styling.

    >>> url = wbemocks.socket.serve("""<!doctype html>
    ... <nav>Word1 Word2 Word3</nav>B""")
    >>> this_browser = browser.Browser()
    >>> this_browser.load(browser.URL(url))
    >>> browser.print_tree(this_browser.nodes)
     <html>
       <body>
         <nav>
           'Word1 Word2 Word3'
         'B'
    >>> browser.print_tree(this_browser.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=30.0, node=<html>)
         BlockLayout(x=13, y=18, width=774, height=30.0, node=<body>)
           BlockLayout(x=13, y=18, width=774, height=15.0, node=<nav>)
           BlockLayout(x=13, y=33.0, width=774, height=15.0, node='B')
    >>> wbemocks.print_list(this_browser.display_list)
    DrawText(top=20.25 left=13 bottom=32.25 text=Word1 font=Font size=12 weight=normal slant=roman style=None)
    DrawText(top=20.25 left=85 bottom=32.25 text=Word2 font=Font size=12 weight=normal slant=roman style=None)
    DrawText(top=20.25 left=157 bottom=32.25 text=Word3 font=Font size=12 weight=normal slant=roman style=None)
    DrawText(top=35.25 left=13 bottom=47.25 text=B font=Font size=12 weight=normal slant=roman style=None)


Test for not using substring match, like class=`blinks`

    >>> url = wbemocks.socket.serve("""<!doctype html>
    ... <nav class="blinks">A</nav>B""")
    >>> this_browser = browser.Browser()
    >>> this_browser.load(browser.URL(url))
    >>> browser.print_tree(this_browser.nodes)
     <html>
       <body>
         <nav class="blinks">
           'A'
         'B'
    >>> browser.print_tree(this_browser.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=30.0, node=<html>)
         BlockLayout(x=13, y=18, width=774, height=30.0, node=<body>)
           BlockLayout(x=13, y=18, width=774, height=15.0, node=<nav class="blinks">)
           BlockLayout(x=13, y=33.0, width=774, height=15.0, node='B')
    >>> wbemocks.print_list(this_browser.display_list)
    DrawText(top=20.25 left=13 bottom=32.25 text=A font=Font size=12 weight=normal slant=roman style=None)
    DrawText(top=35.25 left=13 bottom=47.25 text=B font=Font size=12 weight=normal slant=roman style=None)
