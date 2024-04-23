Tests for WBE Chapter 8 Exercise `GET forms`
============================================

Forms can be submitted via GET requests as well as POST requests. In
GET requests, the form-encoded data is pasted onto the end of the URL,
separated from the path by a question mark, like `/search?q=hi`; GET
form submissions have no body. Implement GET form submissions.

Forms define which submission to use with the `method` attribute,
which will either be `GET` or `POST`. Default to using GET when no
attribute is present.

Ensure not to modify the signature of the URL.request method while 
implementing `GET` form submissions, where form data is appended to
the URL query string.

Test code
---------

Boilerplate.

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> import browser

This is the response to the expected GET request.

    >>> url = 'http://test/chapter8-get-form/submit?name=Ned&comment=Howdily'
    >>> wbemocks.socket.respond_200(url, "Doodily")

This is the form page.

    >>> url2 = wbemocks.socket.serve("""
    ... <form action="/chapter8-get-form/submit" method="GET">
    ...   <p>Name: <input name=name value=Ned></p>
    ...   <p>Comment: <input name=comment value=Howdily></p>
    ...   <p><button>Submit!</button></p>
    ... </form>""")
    >>> this_browser = browser.Browser()
    >>> this_browser.new_tab(browser.URL(url))

Send the defaults using GET.

    >>> this_browser.handle_click(wbemocks.ClickEvent(20, 55 + this_browser.chrome.bottom))
    >>> wbemocks.socket.last_request_path()
    '/chapter8-get-form/submit?name=Ned&comment=Howdily'
    >>> browser.print_tree(this_browser.tabs[0].document.node)
     <html>
       <body>
         'Doodily'

Now lets try a form that does not supply the method attribute.

    >>> url = 'http://test/chapter8-get-form2/submit?food=ribwich'
    >>> wbemocks.socket.respond_200(url, "Mmm")

    >>> url = wbemocks.socket.serve("""
    ... <form action="/chapter8-get-form2/submit">
    ...   <p>Food: <input name=food value=donuts></p>
    ...   <p><button>Submit!</button></p>
    ... </form>""")
    >>> this_browser = browser.Browser()
    >>> this_browser.new_tab(browser.URL(url))

Click on the input and type an answer, then submit the result.

    >>> this_browser.handle_click(wbemocks.ClickEvent(90, 25 + this_browser.chrome.bottom))
    >>> this_browser.focus
    'content'
    >>> this_browser.tabs[0].focus
    <input name="food" value="">

    >>> for c in "ribwich":
    ...   this_browser.handle_key(wbemocks.KeyEvent(c))
    >>> this_browser.handle_click(wbemocks.ClickEvent(20, 42 + this_browser.chrome.bottom))

    >>> wbemocks.socket.last_request_path()
    '/chapter8-get-form2/submit?food=ribwich'
    >>> browser.print_tree(this_browser.tabs[0].document.node)
     <html>
       <body>
         'Mmm'

Double-check that GET forms are not accompanied by the Content-Length header in the request.

    >>> url = 'http://test/chapter8-get-form/submit?name=Ned&comment=Howdily'
    >>> wbemocks.socket.respond_200(url, "Doodily")
    >>> form_page_url = wbemocks.socket.serve("""
    ... <form action="/chapter8-get-form/submit" method="GET">
    ...   <p>Name: <input name=name value=Ned></p>
    ...   <p>Comment: <input name=comment value=Howdily></p>
    ...   <p><button type="submit">Submit!</button></p>
    ... </form>""")
    >>> this_browser = browser.Browser()
    >>> this_browser.new_tab(browser.URL(form_page_url))
    >>> this_browser.handle_click(wbemocks.ClickEvent(20, 55 + this_browser.chrome.bottom))
    >>> command, path, version, headers = wbemocks.socket.parse_last_request(url)
    >>> 'content-length' not in headers
    True
    >>> path
    '/chapter8-get-form/submit?name=Ned&comment=Howdily'