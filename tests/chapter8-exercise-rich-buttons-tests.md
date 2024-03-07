Tests for WBE Chapter 8 Exercise `Rich Buttons`
===============================================

Make it possible for a button to contain arbitrary elements as
children, and render them correctly. The children should be contained
inside the button instead of spilling out---this can make a button
really tall. Think about edge cases, like a button that contains
another button, an input area, or a link, and test real browsers to
see what they do.

You don't need to handle buttons inside buttons---a normal browser
prevents that during parsing. You do, however, need to handle links,
input areas, or even paragraphs inside a button.

To do so, each `<button>` should create a `BlockLayout` child to draw
its contents. All buttons should be `INPUT_WIDHT_PX` by lineheight no
matter their content. (Avoiding this is pretty complex.) You'll still
need to add a little bit of multi-pass layout to avoid issues.

Make sure click handling works correctly when buttons contain
clickable objects like links. For example, in this button

    <button>A <a href=foo.html>link</a> button</button>

it should be possible to click on the link and trigger a navigation,
or click on the button outside the link and trigger a form submission.

Test code
---------

Boilerplate.

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> wbemocks.NORMALIZE_FONT = True
    >>> import browser

First, let's test that a simple button looks normal:

    >>> url = wbemocks.socket.serve("<button>Hello!</button>")
    >>> this_browser = browser.Browser()
    >>> wbemocks.MockCanvas.hide_above(this_browser.chrome.bottom)
    >>> this_browser.new_tab(browser.URL(url))
    >>> browser.print_tree(this_browser.active_tab.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=15.0)
         BlockLayout(x=13, y=18, width=774, height=15.0)
           LineLayout(x=13, y=18, width=774, height=15.0)
             InputLayout(x=13, y=20.25, width=200, height=12, type=button)
               BlockLayout(x=13, y=20.25, width=200, height=15.0)
                 LineLayout(x=13, y=20.25, width=200, height=15.0)
                   TextLayout(x=13, y=22.5, width=72, height=12, word=Hello!)

Note the `BlockLayout` inside the button. It should still produce just
one `DrawText` call:

    >>> wbemocks.print_list(this_browser.active_tab.display_list)
    DrawRect(top=20.25 left=13 bottom=32.25 right=213 color=orange)
    DrawText(top=22.5 left=13 bottom=34.5 text=Hello! font=Font size=12 weight=normal slant=roman style=None)

Next let's put some formatted text in the button:

    >>> url = wbemocks.socket.serve("<button>A<b>bold</b>button</button>")
    >>> this_browser.new_tab(browser.URL(url))
    >>> browser.print_tree(this_browser.active_tab.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=15.0)
         BlockLayout(x=13, y=18, width=774, height=15.0)
           LineLayout(x=13, y=18, width=774, height=15.0)
             InputLayout(x=13, y=20.25, width=200, height=12, type=button)
               BlockLayout(x=13, y=20.25, width=200, height=15.0)
                 LineLayout(x=13, y=20.25, width=200, height=15.0)
                   TextLayout(x=13, y=22.5, width=12, height=12, word=A)
                   TextLayout(x=37, y=22.5, width=48, height=12, word=bold)
                   TextLayout(x=97, y=22.5, width=72, height=12, word=button)
    >>> wbemocks.print_list(this_browser.active_tab.display_list)
    DrawRect(top=20.25 left=13 bottom=32.25 right=213 color=orange)
    DrawText(top=22.5 left=13 bottom=34.5 text=A font=Font size=12 weight=normal slant=roman style=None)
    DrawText(top=22.5 left=37 bottom=34.5 text=bold font=Font size=12 weight=bold slant=roman style=None)
    DrawText(top=22.5 left=97 bottom=34.5 text=button font=Font size=12 weight=normal slant=roman style=None)

We can try more complex formatting. This has four words and will spill
onto two lines. The button should now contain a `BlockLayout` with two
`LineLayout`s inside it. However, it shouldn't be any taller.

    >>> url = wbemocks.socket.serve("<button>An<i>italic<b>bold</b>button</i></button>")
    >>> this_browser.new_tab(browser.URL(url))
    >>> browser.print_tree(this_browser.active_tab.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=15.0)
         BlockLayout(x=13, y=18, width=774, height=15.0)
           LineLayout(x=13, y=18, width=774, height=15.0)
             InputLayout(x=13, y=20.25, width=200, height=12, type=button)
               BlockLayout(x=13, y=20.25, width=200, height=30.0)
                 LineLayout(x=13, y=20.25, width=200, height=15.0)
                   TextLayout(x=13, y=22.5, width=24, height=12, word=An)
                   TextLayout(x=49, y=22.5, width=72, height=12, word=italic)
                   TextLayout(x=133, y=22.5, width=48, height=12, word=bold)
                 LineLayout(x=13, y=35.25, width=200, height=15.0)
                   TextLayout(x=13, y=37.5, width=72, height=12, word=button)
    >>> wbemocks.print_list(this_browser.active_tab.display_list)
    DrawRect(top=20.25 left=13 bottom=32.25 right=213 color=orange)
    DrawText(top=22.5 left=13 bottom=34.5 text=An font=Font size=12 weight=normal slant=roman style=None)
    DrawText(top=22.5 left=49 bottom=34.5 text=italic font=Font size=12 weight=normal slant=italic style=None)
    DrawText(top=22.5 left=133 bottom=34.5 text=bold font=Font size=12 weight=bold slant=italic style=None)
    DrawText(top=37.5 left=13 bottom=49.5 text=button font=Font size=12 weight=normal slant=italic style=None)

Now let's try a link inside a button:

    >>> url = wbemocks.socket.serve("<button><a href=foo>yo</a></button>")
    >>> this_browser.new_tab(browser.URL(url))
    >>> browser.print_tree(this_browser.active_tab.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=15.0)
         BlockLayout(x=13, y=18, width=774, height=15.0)
           LineLayout(x=13, y=18, width=774, height=15.0)
             InputLayout(x=13, y=20.25, width=200, height=12, type=button)
               BlockLayout(x=13, y=20.25, width=200, height=15.0)
                 LineLayout(x=13, y=20.25, width=200, height=15.0)
                   TextLayout(x=13, y=22.5, width=24, height=12, word=yo)
    >>> wbemocks.print_list(this_browser.active_tab.display_list)
    DrawRect(top=20.25 left=13 bottom=32.25 right=213 color=orange)
    DrawText(top=22.5 left=13 bottom=34.5 text=yo font=Font size=12 weight=normal slant=roman style=None)

Finally, let's try an input inside a button:

    >>> url = wbemocks.socket.serve("<button><input value=hi></button>")
    >>> this_browser.new_tab(browser.URL(url))
    >>> browser.print_tree(this_browser.active_tab.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=15.0)
         BlockLayout(x=13, y=18, width=774, height=15.0)
           LineLayout(x=13, y=18, width=774, height=15.0)
             InputLayout(x=13, y=20.25, width=200, height=12, type=button)
               BlockLayout(x=13, y=20.25, width=200, height=15.0)
                 LineLayout(x=13, y=20.25, width=200, height=15.0)
                   InputLayout(x=13, y=22.5, width=200, height=12, type=input)
    >>> wbemocks.print_list(this_browser.active_tab.display_list)
    DrawRect(top=20.25 left=13 bottom=32.25 right=213 color=orange)
    DrawRect(top=22.5 left=13 bottom=34.5 right=213 color=lightblue)
    DrawText(top=22.5 left=13 bottom=34.5 text=hi font=Font size=12 weight=normal slant=roman style=None)

Now let's test click handling. First, let's click a normal button:

    >>> url = "http://test/submit"
    >>> wbemocks.socket.respond_200(url, "OK", method="POST", body="")
    >>> url = wbemocks.socket.serve("""
    ... <form action=/submit method=post>
    ...   <input name=test value=ok>
    ...   <button>yo</button>
    ... </form>""")
    >>> this_browser.new_tab(browser.URL(url))
    >>> this_browser.handle_click(wbemocks.ClickEvent(250, 25 + this_browser.chrome.bottom))
    >>> this_browser.active_tab.url
    URL(scheme=http, host=test, port=80, path='/submit')

Note that clicking on the button submitted the form and navigated to a new page.

Now let's put an `input` into the button and click on that. This
should _not_ click the button (and so not submit the form). We should
instead now be able to type into the input:

    >>> url = wbemocks.socket.serve("""
    ... <form action=/submit method=post>
    ...   <input name=test value=ok>
    ...   <button><input></button>
    ... </form>""")
    >>> this_browser.new_tab(browser.URL(url))
    >>> this_browser.handle_click(wbemocks.ClickEvent(250, 25 + this_browser.chrome.bottom))
    >>> this_browser.active_tab.url
    URL(scheme=http, host=test, port=80, path='/6')
    >>> this_browser.active_tab.focus
    <input value="">
    >>> for i in "Test": this_browser.handle_key(wbemocks.KeyEvent(i))
    >>> this_browser.active_tab.focus
    <input value="Test">
    
Similarly, clicking on a link in a button should navigate to the link,
not submit the form:

    >>> url = "http://test/go"
    >>> wbemocks.socket.respond_200(url, "OK")
    >>> url = wbemocks.socket.serve("""
    ... <form action=/submit method=post>
    ...   <input name=test value=ok>
    ...   <button><a href=/go>go</a></button>
    ... </form>""")
    >>> this_browser.new_tab(browser.URL(url))
    >>> browser.print_tree(this_browser.active_tab.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=15.0)
         BlockLayout(x=13, y=18, width=774, height=15.0)
           BlockLayout(x=13, y=18, width=774, height=15.0)
             LineLayout(x=13, y=18, width=774, height=15.0)
               InputLayout(x=13, y=20.25, width=200, height=12, type=input)
               InputLayout(x=225, y=20.25, width=200, height=12, type=button)
                 BlockLayout(x=225, y=20.25, width=200, height=15.0)
                   LineLayout(x=225, y=20.25, width=200, height=15.0)
                     TextLayout(x=225, y=22.5, width=24, height=12, word=go)
    >>> this_browser.handle_click(wbemocks.ClickEvent(230, 25 + this_browser.chrome.bottom))
    >>> this_browser.active_tab.url
    URL(scheme=http, host=test, port=80, path='/go')

But if we click inside the button but outside the link, that should
submit the form:

    >>> this_browser.new_tab(browser.URL(url))
    >>> this_browser.handle_click(wbemocks.ClickEvent(300, 25 + this_browser.chrome.bottom))
    >>> this_browser.active_tab.url
    URL(scheme=http, host=test, port=80, path='/submit')
