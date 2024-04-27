Tests for WBE Chapter 8
=======================

Chapter 8 (Sending Information to Servers) introduces forms and shows how
to implement simple input and button elements, plus submit forms to the server.
It also includes the first implementation of an HTTP server, in order to show
how the server processes form submissions.

You'll need the following `__repr__` method on `InputLayout`:

```
class InputLayout:
    def __repr__(self):
        return "InputLayout(x={}, y={}, width={}, height={}, tag={})".format(
            self.x, self.y, self.width, self.height, self.node.tag)
```

Testing request
===============

Boilerplate:

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> import browser

This chapter adds the ability to submit a POST request in addition to a GET
one.

    >>> url = 'http://test/chapter8-base/submit'
    >>> request_body = "name=1&comment=2%3D3"
    >>> len(request_body)
    20
    >>> wbemocks.socket.respond(url, b"HTTP/1.0 200 OK\r\n" +
    ... b"Header1: Value1\r\n\r\n" +
    ... b"<div>Form submitted</div>", method="POST", body=request_body)
    >>> body = browser.URL(url).request(payload=request_body)
    >>> req = wbemocks.socket.last_request(url).decode().lower()
    >>> req.startswith("post")
    True
    >>> "content-length: 20" in req
    True
    >>> req.endswith('name=1&comment=2%3d3')
    True


Testing InputLayout
===================

    >>> url2 = browser.URL(wbemocks.socket.serve("""
    ... <form action="/chapter8-base/submit" method="POST">
    ...   <p>Name: <input name=name value=1></p>
    ...   <p>Comment: <input name=comment value="2=3"></p>
    ...   <p><button>Submit!</button></p>
    ... </form>"""))
    >>> this_browser = browser.Browser()
    >>> this_browser.new_tab(url2)
    >>> browser.print_tree(this_browser.tabs[0].document.node)
     <html>
       <body>
         <form action="/chapter8-base/submit" method="POST">
           <p>
             'Name: '
             <input name="name" value="1">
           <p>
             'Comment: '
             <input name="comment" value="2=3">
           <p>
             <button>
               'Submit!'
    >>> browser.print_tree(this_browser.tabs[0].document) #doctest: +ELLIPSIS
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=45.0, node=<html>)
         BlockLayout(x=13, y=18, width=774, height=45.0, node=<body>)
           BlockLayout(x=13, y=18, width=774, height=45.0, node=<form action="/chapter8-base/submit" method="POST">)
             BlockLayout(x=13, y=18, width=774, height=15.0, node=<p>)
               LineLayout(x=13, y=18, width=774, height=15.0)
                 TextLayout(x=13, y=20.25, width=60, height=12, word=Name:)
                 InputLayout(x=85, y=20.25, width=200, height=12, node=<input name="name" value="1">)
             BlockLayout(x=13, y=33.0, width=774, height=15.0, node=<p>)
               LineLayout(x=13, y=33.0, width=774, height=15.0)
                 TextLayout(x=13, y=35.25, width=96, height=12, word=Comment:)
                 InputLayout(x=121, y=35.25, width=200, height=12, node=<input name="comment" value="2=3">)
             BlockLayout(x=13, y=48.0, width=774, height=15.0, node=<p>)
               LineLayout(x=13, y=48.0, width=774, height=15.0)
                 InputLayout(x=13, y=50.25, width=200, height=12, node=<button>)...

The display list of a button should include its contents, and the display list
of a text input should be its `value` attribute:

    >>> form = this_browser.tabs[0].document.children[0].children[0].children[0]
    >>> text_input = form.children[0].children[0].children[1]
    >>> button = form.children[2].children[0].children[0]
    >>> wbemocks.print_list(text_input.paint())
    DrawRect(top=20.25 left=85 bottom=32.25 right=285 color=lightblue)
    DrawText(top=20.25 left=85 bottom=32.25 text=1 font=Font size=12 weight=normal slant=roman style=None)

I'm not testing the button because that changes with the "Rich
Buttons" exercise.

Testing form submission
=======================

Forms are submitted via a click on the submit button.

    >>> this_browser.handle_click(wbemocks.ClickEvent(20, 55 + this_browser.chrome.bottom))
    >>> browser.print_tree(this_browser.tabs[0].document.node)
     <html>
       <body>
         <div>
           'Form submitted'

Testing the server
==================

    >>> import server

The server handles a GET request to the "/" URL:

    >>> server.do_request("GET", "/", {}, "")
    ('200 OK', '<!doctype html><form action=add method=post><p><input name=guest></p><p><button>Sign the book!</button></p></form><p>Pavel was here</p>')

GET requests to other URLs return a 404 page:

    >>> server.do_request("GET", "/unknown", {}, "")
    ('404 Not Found', '<!doctype html><h1>GET /unknown not found!</h1>')

A POST request is supported at the "/add" URL, which will parse out the `guest`
parameter from the body, insert it into the guestbook, and return it as part of
the response page:

    >>> server.do_request("POST", "/add", {}, "guest=Chris")
    ('200 OK', '<!doctype html><form action=add method=post><p><input name=guest></p><p><button>Sign the book!</button></p></form><p>Pavel was here</p><p>Chris</p>')

POST requsts to other URLs return 404 pages:

    >>> server.do_request("POST", "/", {}, "")
    ('404 Not Found', '<!doctype html><h1>POST / not found!</h1>')

In `BlockLayout.recurse`, do not recurse into buttons.

    >>> url = wbemocks.socket.serve("""
    ... <form action="submit" method="POST">
    ...   <p>Text before button</p>
    ...   <button>Submit</button>
    ...   <p>Text after button</p>
    ... </form>""")
    >>> this_browser = browser.Browser()
    >>> this_browser.new_tab(browser.URL(url))
    >>> browser.print_tree(this_browser.active_tab.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=45.0, node=<html>)
         BlockLayout(x=13, y=18, width=774, height=45.0, node=<body>)
           BlockLayout(x=13, y=18, width=774, height=45.0, node=<form action="submit" method="POST">)
             BlockLayout(x=13, y=18, width=774, height=15.0, node=<p>)
               LineLayout(x=13, y=18, width=774, height=15.0)
                 TextLayout(x=13, y=20.25, width=48, height=12, word=Text)
                 TextLayout(x=73, y=20.25, width=72, height=12, word=before)
                 TextLayout(x=157, y=20.25, width=72, height=12, word=button)
             BlockLayout(x=13, y=33.0, width=774, height=15.0, node=<button>)
               LineLayout(x=13, y=33.0, width=774, height=15.0)
                 InputLayout(x=13, y=35.25, width=200, height=12, node=<button>)...
             BlockLayout(x=13, y=48.0, width=774, height=15.0, node=<p>)
               LineLayout(x=13, y=48.0, width=774, height=15.0)
                 TextLayout(x=13, y=50.25, width=48, height=12, word=Text)
                 TextLayout(x=73, y=50.25, width=60, height=12, word=after)
                 TextLayout(x=145, y=50.25, width=72, height=12, word=button)

Verify that when clicking anywhere within a form, excluding buttons or input elements, the form isn't submitted.

    >>> form_html = """
    ... <form action="/submit" method="POST">
    ...     <p>Click here should do nothing:</p>
    ...     <div style="width: 300px; height: 100px;"></div>
    ...     <input type="submit" value="Submit">
    ... </form>"""
    >>> url = "http://test/test-form-works"
    >>> wbemocks.socket.respond_ok(url, form_html)
    >>> this_browser = browser.Browser()
    >>> this_browser.new_tab(browser.URL(url))
    >>> this_browser.handle_click(wbemocks.ClickEvent(150, 60 + this_browser.chrome.bottom))
    >>> print(this_browser.tabs[0].url)
    http://test/test-form-works

    >>> wbemocks.socket.made_request("http://test/submit")
    False
