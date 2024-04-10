Tests for WBE Chapter 8 Exercise `Tab`
============================================

In most browsers, the `<Tab>` key (on your keyboard) moves focus from
one input field to the next. Implement this behavior in your browser.
The “tab order” of input elements should be the same as the order of
`<input>` elements on the page. You can also add support for the
`tabindex` property, which lets a web page change this tab order.

You don't need to support `tabindex`. Name the method in the `Browser`
class that handles the tab event `handle_tab`.

Test code
---------

Boilerplate.

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> import browser

This is the form page.

    >>> url = wbemocks.socket.serve("""
    ... <form action="/chapter8-tab/submit">
    ...   <p>Name: <input name=name value=1></p>
    ...   <p>Comment: <input name=comment value="2=3"></p>
    ...   <p>Sign: <input name=sign value=ares></p>
    ...   <p><button>Submit!</button></p>
    ... </form>""")
    >>> this_browser = browser.Browser()
    >>> this_browser.new_tab(browser.URL(url))

Click on the name field.

    >>> this_browser.handle_click(wbemocks.ClickEvent(90, 25 + this_browser.chrome.bottom))
    >>> this_browser.focus
    'content'
    >>> this_browser.tabs[0].focus
    <input name="name" value="">

Tab to the comment field, which should be emptied upon selection.

    >>> this_browser.handle_tab(wbemocks.Event())
    >>> this_browser.focus
    'content'
    >>> this_browser.tabs[0].focus
    <input name="comment" value="">

Tab to the sign field.

    >>> this_browser.handle_tab(wbemocks.Event())
    >>> this_browser.focus
    'content'
    >>> this_browser.tabs[0].focus
    <input name="sign" value="">

Tab should cycle back to the name field.

    >>> this_browser.handle_tab(wbemocks.Event())
    >>> this_browser.focus
    'content'
    >>> this_browser.tabs[0].focus
    <input name="name" value="">
