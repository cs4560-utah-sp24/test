Tests for WBE Chapter 8
=======================

Chapter 8 (Sending Information to Servers) introduces forms and shows how
to implement simple input and button elements, plus submit forms to the server.
It also includes the first implementation of an HTTP server, in order to show
how the server processes form submissions.

    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> test.NORMALIZE_FONT = True
    >>> import browser

Testing request
===============

This chapter adds the ability to submit a POST request in addition to a GET
one.

    >>> url = 'http://test.test/chapter8-base/submit'
    >>> request_body = "name=1&comment=2%3D3"
    >>> test.socket.respond(url, b"HTTP/1.0 200 OK\r\n" +
    ... b"Header1: Value1\r\n\r\n" +
    ... b"<div>Form submitted</div>", method="POST", body=request_body)
    >>> headers, body = browser.request(url, payload=request_body)
    >>> req = test.socket.last_request(url).decode().lower()
    >>> req.startswith("post")
    True
    >>> "content-length: 20" in req
    True
    >>> req.endswith('name=1&comment=2%3d3')
    True


Testing InputLayout
===================

    >>> url2 = 'http://test.test/chapter8-base/example'
    >>> test.socket.respond(url2, b"HTTP/1.0 200 OK\r\n" +
    ... b"Header1: Value1\r\n\r\n" +
    ... b"<form action=\"/chapter8-base/submit\" method=\"POST\">" +
    ... b"  <p>Name: <input name=name value=1></p>" +
    ... b"  <p>Comment: <input name=comment value=\"2=3\"></p>" +
    ... b"  <p><button>Submit!</button></p>" +
    ... b"</form>")
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url2)
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
                 TextLayout(x=13, y=35.25, width=96, height=12, font=Font size=12 weight=normal slant=roman style=None)
                 InputLayout(x=121, y=35.25, width=200, height=12)
             InlineLayout(x=13, y=48.0, width=774, height=15.0)
               LineLayout(x=13, y=48.0, width=774, height=15.0)
                 InputLayout(x=13, y=50.25, width=200, height=12)

The display list of a button should include its contents, and the display list
of a text input should be its `value` attribute:

    >>> form = this_browser.tabs[0].document.children[0].children[0].children[0]
    >>> text_input = form.children[0].children[0].children[1]
    >>> button = form.children[2].children[0].children[0]
    >>> display_list = []
    >>> text_input.paint(display_list)
    >>> display_list
    [DrawRect(top=20.25 left=85 bottom=32.25 right=285 color=lightblue), DrawText(top=20.25 left=85 bottom=32.25 text=1 font=Font size=12 weight=normal slant=roman style=None)]
    >>> display_list = []
    >>> button.paint(display_list)
    >>> display_list
    [DrawRect(top=50.25 left=13 bottom=62.25 right=213 color=orange), DrawText(top=50.25 left=13 bottom=62.25 text=Submit! font=Font size=12 weight=normal slant=roman style=None)]

Testing form submission
=======================

Forms are submitted via a click on the submit button.

    >>> this_browser.handle_click(test.Event(20, 55 + browser.CHROME_PX))
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

