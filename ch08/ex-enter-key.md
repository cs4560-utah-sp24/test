Tests for WBE Chapter 8 Exercise `Enter key`
============================================

In most browsers, if you hit the “Enter” or “Return” key while inside
a text entry, that submits the form that the text entry was in. Add
this feature to your browser.

Test code
---------

Boilerplate.

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> import browser

This is the response to the expected POST request.

    >>> url = 'http://test/chapter8-enter/submit'
    >>> request_body = "name=Killroy&comment=2%3D3"
    >>> wbemocks.socket.respond(url, b"HTTP/1.0 200 OK\r\n\r\n" +
    ... b"<div>Form submitted</div>", method="POST", body=request_body)

This is the form page.

    >>> url2 = wbemocks.socket.serve("""
    ... <form action="/chapter8-enter/submit" method="POST">
    ...   <p>Name: <input name=name value=1></p>
    ...   <p>Comment: <input name=comment value="2=3"></p>
    ...   <p><button>Submit!</button></p>
    ... </form>""")
    >>> this_browser = browser.Browser()
    >>> this_browser.new_tab(browser.URL(url2))

Pressing enter when there is no focus should not change anything.

    >>> this_browser.focus == None
    True
    >>> this_browser.handle_enter(wbemocks.Event())
    >>> this_browser.focus == None
    True

Clicking on the input should clear its content and set focus

    >>> this_browser.handle_click(wbemocks.ClickEvent(90, 25 + this_browser.chrome.bottom))
    >>> this_browser.focus
    'content'
    >>> this_browser.tabs[0].focus
    <input name="name" value="">

Type in a response then press enter to perform the POST request.
This will be matched against the earlier description.

    >>> for c in "Killroy":
    ...   this_browser.handle_key(wbemocks.KeyEvent(c))
    >>> this_browser.handle_enter(wbemocks.Event())

Examine the post request.

    >>> req = wbemocks.socket.last_request(url).decode().lower()
    >>> req.startswith("post")
    True
    >>> "content-length: 26" in req
    True
    >>> req.endswith('name=killroy&comment=2%3d3')
    True
