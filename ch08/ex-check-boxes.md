Tests for WBE Chapter 8 Exercise `Check boxes`
============================================

In HTML, `input` elements have a `type` attribute. When set to `checkbox`,
the input element looks like a checkbox; it’s checked if the `checked`
attribute is set, and unchecked otherwise. When the form is submitted,
a checkbox’s `name=value` pair is included only if the checkbox is
checked. (If the checkbox has no `value` attribute, the default is the
string `on`.)

Artistically the checkbox can be drawn how you want. Functionally the
checkbox should be a 16 by 16 pixel region which changes state when
clicked.

You'll need to extend your `InputLayout`'s `__repr__` method like so:

```
class InputLayout:
    def __repr__(self):
        if self.node.tag == "input" and self.node.attributes.get("type", "text") == "checkbox":
            if "checked" in self.node.attributes:
                extra = ", checked"
            else:
                extra = ", unchecked"
        else:
            extra = ""
        return "InputLayout(x={}, y={}, width={}, height={}, tag={}{})".format(
            self.x, self.y, self.width, self.height, self.node.tag, extra)
```

Test code
---------

Boilerplate.

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> import browser

This is the response to the expected POST request.

    >>> url = 'http://test/chapter8-check-boxes/submit'
    >>> request_body = "name=Bob"
    >>> wbemocks.socket.respond_200(url, \
    ...   "<div>Form submitted</div>", \
    ...   method="POST", body=request_body)

This is the form page.

    >>> url2 = wbemocks.socket.serve("""
    ... <form action="/chapter8-check-boxes/submit" method="POST">
    ...   <p>Name: <input name=name value=Bob></p>
    ...   <p>Checkbox: <input name=checkey type=checkbox></p>
    ...   <p><button>Submit!</button></p>
    ... </form>""")
    >>> this_browser = browser.Browser()
    >>> this_browser.new_tab(browser.URL(url2))
    >>> browser.print_tree(this_browser.active_tab.document) #doctest: +ELLIPSIS
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=45.0, node=<html>)
         BlockLayout(x=13, y=18, width=774, height=45.0, node=<body>)
           BlockLayout(x=13, y=18, width=774, height=45.0, node=<form action="/chapter8-check-boxes/submit" method="POST">)
             BlockLayout(x=13, y=18, width=774, height=15.0, node=<p>)
               LineLayout(x=13, y=18, width=774, height=15.0)
                 TextLayout(x=13, y=20.25, width=60, height=12, word=Name:)
                 InputLayout(x=85, y=20.25, width=200, height=12, node=<input name="name" value="Bob">)
             BlockLayout(x=13, y=33.0, width=774, height=15.0, node=<p>)
               LineLayout(x=13, y=33.0, width=774, height=15.0)
                 TextLayout(x=13, y=35.25, width=108, height=12, word=Checkbox:)
                 InputLayout(x=133, y=35.25, width=16, height=16, node=<input name="checkey" type="checkbox">)
             BlockLayout(x=13, y=48.0, width=774, height=15.0, node=<p>)
               LineLayout(x=13, y=48.0, width=774, height=15.0)
                 InputLayout(x=13, y=50.25, width=200, height=12, node=<button>)...

Send the form with the box unchecked. This will be matched against the earlier description.

    >>> for c in "Killroy":
    ...   this_browser.handle_key(wbemocks.KeyEvent(c))
    >>> this_browser.handle_click(wbemocks.ClickEvent(20, 56 + this_browser.chrome.bottom))

Now we are looking for a response where the checkbox is set.

    >>> request_body = "name=Alice&checkey=on"
    >>> wbemocks.socket.respond_200(url, \
    ...   "<div>Form submitted</div>", \
    ...   method="POST", body=request_body)

Make a new browser, load the page, enter a new name, click the
checkbox.

    >>> this_browser = browser.Browser()
    >>> this_browser.new_tab(browser.URL(url2))
    >>> this_browser.handle_click(wbemocks.ClickEvent(90, 25 + this_browser.chrome.bottom))
    >>> this_browser.focus
    'content'
    >>> this_browser.tabs[0].focus
    <input name="name" value="">
    >>> for c in "Alice":
    ...   this_browser.handle_key(wbemocks.KeyEvent(c))
    >>> this_browser.handle_click(wbemocks.ClickEvent(141, 43  + this_browser.chrome.bottom))
    >>> browser.print_tree(this_browser.active_tab.document) #doctest: +ELLIPSIS
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=45.0, node=<html>)
         BlockLayout(x=13, y=18, width=774, height=45.0, node=<body>)
           BlockLayout(x=13, y=18, width=774, height=45.0, node=<form action="/chapter8-check-boxes/submit" method="POST">)
             BlockLayout(x=13, y=18, width=774, height=15.0, node=<p>)
               LineLayout(x=13, y=18, width=774, height=15.0)
                 TextLayout(x=13, y=20.25, width=60, height=12, word=Name:)
                 InputLayout(x=85, y=20.25, width=200, height=12, node=<input name="name" value="Alice">)
             BlockLayout(x=13, y=33.0, width=774, height=15.0, node=<p>)
               LineLayout(x=13, y=33.0, width=774, height=15.0)
                 TextLayout(x=13, y=35.25, width=108, height=12, word=Checkbox:)
                 InputLayout(x=133, y=35.25, width=16, height=16, node=<input name="checkey" type="checkbox" checked="">)
             BlockLayout(x=13, y=48.0, width=774, height=15.0, node=<p>)
               LineLayout(x=13, y=48.0, width=774, height=15.0)
                 InputLayout(x=13, y=50.25, width=200, height=12, node=<button>)...
                 
Now the form should be sent without the checkbox checked:

    >>> this_browser.handle_click(wbemocks.ClickEvent(20, 56 + this_browser.chrome.bottom))
