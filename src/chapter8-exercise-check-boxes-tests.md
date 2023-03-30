Tests for WBE Chapter 8 Exercise `Check boxes`
============================================

Description
-----------

In HTML, input elements have a type attribute.
When set to checkbox, the input element looks like a checkbox; it’s checked if
  the checked attribute is set, and unchecked otherwise.
When the form is submitted, a checkbox’s name=value pair is included only if
  the checkbox is checked. (If the checkbox has no value attribute, the default
  is the string on.)


Extra Requirements
------------------
* Artistically the checkbox can be drawn how you want.
* Functionally the checkbox should be a 16 by 16 pixel region which changes
  state when clicked.


Test code
---------

Boilerplate.

    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> import browser

This is the response to the expected POST request.

    >>> url = 'http://test.test/chapter8-check-boxes/submit'
    >>> request_body = "name=Bob"
    >>> test.socket.respond(url, b"HTTP/1.0 200 OK\r\n\r\n" +
    ... b"<div>Form submitted</div>", method="POST", body=request_body)

This is the form page.

    >>> url = 'http://test.test/chapter8-check-boxes/example'
    >>> body = ("<form action=\"/chapter8-check-boxes/submit\" method=\"POST\">" +
    ...         "  <p>Name: <input name=name value=Bob></p>" +
    ...         "  <p>Checkbox: <input name=checkey type=checkbox></p>" +
    ...         "  <p><button>Submit!</button></p>" +
    ...         "</form>")
    >>> test.socket.respond_200(url, body)
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)

Send the form.
This will be matched against the earlier description.

    >>> for c in "Killroy":
    ...   this_browser.handle_key(test.key_event(c))
    >>> this_browser.handle_click(test.Event(20, 55 + browser.CHROME_PX))


Now we are looking for a response where the checkbox is set.

    >>> url = 'http://test.test/chapter8-check-boxes/submit'
    >>> request_body = "name=Alice&checkey=on"
    >>> test.socket.respond(url, b"HTTP/1.0 200 OK\r\n\r\n" +
    ... b"<div>Form submitted</div>", method="POST", body=request_body)

Make a new browser, load the page, enter a new name, click the checkbox, and
    send the form.

    >>> this_browser = browser.Browser()
    >>> this_browser.load('http://test.test/chapter8-check-boxes/example')
    >>> this_browser.handle_click(test.Event(90, 25 + browser.CHROME_PX))
    >>> this_browser.focus
    'content'
    >>> this_browser.tabs[0].focus
    <input name="name" value="">
    >>> for c in "Alice":
    ...   this_browser.handle_key(test.key_event(c))

    >>> this_browser.handle_click(test.Event(141, 43  + browser.CHROME_PX))
    >>> this_browser.handle_click(test.Event(20, 56 + browser.CHROME_PX))


    113.0 56.25
