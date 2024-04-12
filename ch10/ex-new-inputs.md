Tests for WBE Chapter 10 Exercise `New inputs`
============================================

Add support for hidden and password input elements. Hidden inputs
shouldn’t show up or take up space, while password input elements
should show ther contents as stars instead of characters.

To hide the input element set its width and height to `0.0`

Tests
-----

Boilerplate.

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> wbemocks.NO_CACHE = True
    >>> wbemocks.NORMALIZE_FONT = True
    >>> import browser

Make a page with a hidden input element.

    >>> url = "http://wbemocks.wbemocks.chapter10-new-inputs/"
    >>> page = """<!doctype html>
    ... <form action="/tricky" method=POST>
    ...   <p>Not hidden: <input name=visible value=1></p>
    ...   <p>Hidden: <input type=hidden name=invisible value=doNotShowMe></p>
    ...   <p><button>Submit!</button></p>
    ... </form>"""
    >>> wbemocks.socket.respond_ok(url, page)
    >>> wbemocks.socket.respond(url + "tricky", b"HTTP/1.0 200 OK\r\n\r\nEmpty", "POST")

The hidden element should not show up.
There are many ways to achieve this effect, we will set the width and height of
    the element to 0.0.

    >>> this_browser = browser.Browser()
    >>> this_browser.new_tab(browser.URL(url))
    >>> browser.print_tree(this_browser.tabs[0].document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=45.0, node=<html>)
         BlockLayout(x=13, y=18, width=774, height=45.0, node=<body>)
           BlockLayout(x=13, y=18, width=774, height=45.0, node=<form action="/tricky" method="POST">)
             BlockLayout(x=13, y=18, width=774, height=15.0, node=<p>)
               LineLayout(x=13, y=18, width=774, height=15.0)
                 TextLayout(x=13, y=20.25, width=36, height=12, word=Not)
                 TextLayout(x=61, y=20.25, width=84, height=12, word=hidden:)
                 InputLayout(x=157, y=20.25, width=200, height=12, node=<input name="visible" value="1">)
             BlockLayout(x=13, y=33.0, width=774, height=15.0, node=<p>)
               LineLayout(x=13, y=33.0, width=774, height=15.0)
                 TextLayout(x=13, y=35.25, width=84, height=12, word=Hidden:)
                 InputLayout(x=109, y=35.25, width=0.0, height=0.0, node=<input type="hidden" name="invisible" value="doNotShowMe">)
             BlockLayout(x=13, y=48.0, width=774, height=15.0, node=<p>)
               LineLayout(x=13, y=48.0, width=774, height=15.0)
                 InputLayout(x=13, y=50.25, width=200, height=12, node=<button>)...

Submission of the form should still pass along the value.

    >>> this_browser.handle_click(wbemocks.ClickEvent(21, this_browser.chrome.bottom+58))
    >>> req = wbemocks.socket.last_request(url + "tricky").decode().lower()
    >>> req.startswith("post")
    True
    >>> "content-length: 31" in req
    True
    >>> req.endswith("visible=1&invisible=donotshowme")
    True

Make a page with a password input element.

    >>> url = "http://wbemocks.wbemocks.chapter10-new-inputs/"
    >>> page = """<!doctype html>
    ... <form action="/login" method=POST>
    ...   <p>Name: <input name=name value=Skroob></p>
    ...   <p>Password: <input type=password name=password value=12345></p>
    ...   <p><button>Submit!</button></p>
    ... </form>"""
    >>> wbemocks.socket.respond_ok(url, page)
    >>> wbemocks.socket.respond(url + "login", b"HTTP/1.0 200 OK\r\n\r\nEmpty", "POST")

The password element should be all `*`.

    >>> this_browser = browser.Browser()
    >>> this_browser.new_tab(browser.URL(url))
    >>> browser.print_tree(this_browser.tabs[0].document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=45.0, node=<html>)
         BlockLayout(x=13, y=18, width=774, height=45.0, node=<body>)
           BlockLayout(x=13, y=18, width=774, height=45.0, node=<form action="/login" method="POST">)
             BlockLayout(x=13, y=18, width=774, height=15.0, node=<p>)
               LineLayout(x=13, y=18, width=774, height=15.0)
                 TextLayout(x=13, y=20.25, width=60, height=12, word=Name:)
                 InputLayout(x=85, y=20.25, width=200, height=12, node=<input name="name" value="Skroob">)
             BlockLayout(x=13, y=33.0, width=774, height=15.0, node=<p>)
               LineLayout(x=13, y=33.0, width=774, height=15.0)
                 TextLayout(x=13, y=35.25, width=108, height=12, word=Password:)
                 InputLayout(x=133, y=35.25, width=200, height=12, node=<input type="password" name="password" value="12345">)
             BlockLayout(x=13, y=48.0, width=774, height=15.0, node=<p>)
               LineLayout(x=13, y=48.0, width=774, height=15.0)
                 InputLayout(x=13, y=50.25, width=200, height=12, node=<button>)...

    >>> document = this_browser.active_tab.document
    >>> form = document.children[0].children[0].children[0]
    >>> para = form.children[1].children[0]
    >>> pswd = para.children[1]
    >>> wbemocks.print_list(pswd.paint())
    DrawRect(top=35.25 left=133 bottom=47.25 right=333 color=lightblue)
    DrawText(top=35.25 left=133 bottom=47.25 text=***** font=Font size=12 weight=normal slant=roman style=None)


Submission of the form should still pass along the value.

    >>> this_browser.handle_click(wbemocks.ClickEvent(21, this_browser.chrome.bottom+58))
    >>> req = wbemocks.socket.last_request(url + "login").decode().lower()
    >>> req.startswith("post")
    True
    >>> "content-length: 26" in req
    True
    >>> req.endswith("name=skroob&password=12345")
    True
