Tests for WBE Chapter 10 Exercise `New inputs`
============================================

Description
-----------
Add support for hidden and password input elements.
Hidden inputs shouldn’t show up or take up space, while password input elements
    should show ther contents as stars instead of characters.


Extra Requirements
------------------
* To hide the input element set its width and height to `0.0`


Test code
---------

Boilerplate.

    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> test.NO_CACHE = True
    >>> test.NORMALIZE_FONT = True
    >>> import browser

Make a page with a hidden input element.

    >>> url = "http://test.test.chapter10-new-inputs/"
    >>> page = """<!doctype html>
    ... <form action="/tricky" method=POST>
    ...   <p>Not hidden: <input name=visible value=1></p>
    ...   <p>Hidden: <input type=hidden name=invisible value=doNotShowMe></p>
    ...   <p><button>Submit!</button></p>
    ... </form>"""
    >>> test.socket.respond_ok(url, page)
    >>> test.socket.respond(url + "tricky", b"HTTP/1.0 200 OK\r\n\r\nEmpty", "POST")

The hidden element should not show up.
There are many ways to achieve this effect, we will set the width and height of
    the element to 0.0.

    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    >>> browser.print_tree(this_browser.tabs[0].document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=45.0)
         BlockLayout(x=13, y=18, width=774, height=45.0)
           BlockLayout(x=13, y=18, width=774, height=45.0)
             InlineLayout(x=13, y=18, width=774, height=15.0)
               LineLayout(x=13, y=18, width=774, height=15.0)
                 TextLayout(x=13, y=20.25, width=36, height=12, font=Font size=12 weight=normal slant=roman style=None)
                 TextLayout(x=61, y=20.25, width=84, height=12, font=Font size=12 weight=normal slant=roman style=None)
                 InputLayout(x=157, y=20.25, width=200, height=12)
             InlineLayout(x=13, y=33.0, width=774, height=15.0)
               LineLayout(x=13, y=33.0, width=774, height=15.0)
                 TextLayout(x=13, y=35.25, width=84, height=12, font=Font size=12 weight=normal slant=roman style=None)
                 InputLayout(x=109, y=35.25, width=0.0, height=0.0)
             InlineLayout(x=13, y=48.0, width=774, height=15.0)
               LineLayout(x=13, y=48.0, width=774, height=15.0)
                 InputLayout(x=13, y=50.25, width=200, height=12)

Submission of the form should still pass along the value.

    >>> this_browser.handle_click(test.Event(21, 100+58))
    >>> req = test.socket.last_request(url + "tricky").decode().lower()
    >>> req.startswith("post")
    True
    >>> "content-length: 31" in req
    True
    >>> req.endswith("visible=1&invisible=donotshowme")
    True

Make a page with a password input element.

    >>> url = "http://test.test.chapter10-new-inputs/"
    >>> page = """<!doctype html>
    ... <form action="/login" method=POST>
    ...   <p>Name: <input name=name value=Skroob></p>
    ...   <p>Password: <input type=password name=password value=12345></p>
    ...   <p><button>Submit!</button></p>
    ... </form>"""
    >>> test.socket.respond_ok(url, page)
    >>> test.socket.respond(url + "login", b"HTTP/1.0 200 OK\r\n\r\nEmpty", "POST")

The password element should be all `*`.

    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    >>> browser.print_tree(this_browser.tabs[0].document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=45.0)
         BlockLayout(x=13, y=18, width=774, height=45.0)
           BlockLayout(x=13, y=18, width=774, height=45.0)
             InlineLayout(x=13, y=18, width=774, height=15.0)
               LineLayout(x=13, y=18, width=774, height=15.0)
                 TextLayout(x=13, y=20.25, width=60, height=12, font=Font size=12 weight=normal slant=roman style=None)
                 InputLayout(x=85, y=20.25, width=200, height=12)
             InlineLayout(x=13, y=33.0, width=774, height=15.0)
               LineLayout(x=13, y=33.0, width=774, height=15.0)
                 TextLayout(x=13, y=35.25, width=108, height=12, font=Font size=12 weight=normal slant=roman style=None)
                 InputLayout(x=133, y=35.25, width=200, height=12)
             InlineLayout(x=13, y=48.0, width=774, height=15.0)
               LineLayout(x=13, y=48.0, width=774, height=15.0)
                 InputLayout(x=13, y=50.25, width=200, height=12)

    >>> form = this_browser.tabs[0].document.children[0].children[0].children[0]
    >>> para = form.children[1].children[0]
    >>> pswd = para.children[1]
    >>> dl = list()
    >>> pswd.paint(dl)
    >>> dl #doctest: +NORMALIZE_WHITESPACE
    [DrawRect(top=35.25 left=133 bottom=47.25 right=333 color=lightblue),
     DrawText(top=35.25 left=133 bottom=47.25 text=***** font=Font size=12 weight=normal slant=roman style=None)]


Submission of the form should still pass along the value.

    >>> this_browser.handle_click(test.Event(21, 100+58))
    >>> req = test.socket.last_request(url + "login").decode().lower()
    >>> req.startswith("post")
    True
    >>> "content-length: 26" in req
    True
    >>> req.endswith("name=skroob&password=12345")
    True

