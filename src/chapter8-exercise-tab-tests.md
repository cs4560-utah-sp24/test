Tests for WBE Chapter 8 Exercise `Tab`
============================================

Description
-----------

In most browsers, the `<Tab>` key (on your keyboard) moves focus from one input
  field to the next.
Implement this behavior in your browser.
The “tab order” of input elements should be the same as the order of `<input>`
  elements on the page.
~~You can also add support for the tabindex property, which lets a web page
  change this tab order.~~


Extra Requirements
------------------
* Name the method in the `Browser` class that handles the tab event
  `handle_tab`


Test code
---------

Boilerplate.

    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> import browser

This is the form page.

    >>> url = 'http://test.test/chapter8-tab/example'
    >>> body = ("<form action=\"/chapter8-tab/submit\">" +
    ...         "  <p>Name: <input name=name value=1></p>" +
    ...         "  <p>Comment: <input name=comment value=\"2=3\"></p>" +
    ...         "  <p>Sign: <input name=sign value=ares></p>" +
    ...         "  <p><button>Submit!</button></p>" +
    ...         "</form>")
    >>> test.socket.respond_200(url, body)
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)

Click on the name field.

    >>> this_browser.handle_click(test.Event(90, 25 + browser.CHROME_PX))
    >>> this_browser.focus
    'content'
    >>> this_browser.tabs[0].focus
    <input name="name" value="">

Tab to the comment field, which should be emptied upon selection.

    >>> this_browser.handle_tab(test.tab_event())
    >>> this_browser.focus
    'content'
    >>> this_browser.tabs[0].focus
    <input name="comment" value="">

Tab to the sign field.

    >>> this_browser.handle_tab(test.tab_event())
    >>> this_browser.focus
    'content'
    >>> this_browser.tabs[0].focus
    <input name="sign" value="">

Tab should cycle back to the name field.

    >>> this_browser.handle_tab(test.tab_event())
    >>> this_browser.focus
    'content'
    >>> this_browser.tabs[0].focus
    <input name="name" value="">
