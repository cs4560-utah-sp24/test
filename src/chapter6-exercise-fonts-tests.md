Tests for WBE Chapter 6 Exercise `Fonts`
=======================

Description
-----------

Implement the font-family property, an inheritable property that names which
  font should be used in an element.
Make code fonts use some nice monospaced font like Courier.


Please modify the `__repr__` method of your `DrawText` class to contain
`return "DrawText(top={} left={} bottom={} text={} font={})".format(self.top, self.left, self.bottom, self.text, self.font)`

    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> import browser
    >>> def print_style(style):
    ...     for key in sorted(style):
    ...         val = style[key]
    ...         print(f"{key}: {val}")

The default font-family should be "Times".

    >>> html = browser.Element("html", {}, None)
    >>> body = browser.Element("body", {}, html)
    >>> div = browser.Element("div", {}, body)
    >>> browser.style(html, [])
    >>> print_style(html.style)
    color: black
    font-family: Times
    font-size: 16px
    font-style: normal
    font-weight: normal

The font for `code` elements should be "Courier".

    >>> url = 'http://test.test/chapter6_example3'
    >>> test.socket.respond_200(url, body="<code> code </code>")
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    >>> this_browser.display_list
    [DrawText(top=20.25 left=13 bottom=32.25 text=code font=Font size=12 weight=normal slant=roman style=None family=Courier)]

Inheritance should be handled.

    >>> body = ('<p style="font-family:foo">' +
    ...         '<span>A</span>' +
    ...         '<span style="font-family:bar"> B </span>'
    ...         '</p>')
    >>> url = 'http://test.test/chapter6_example4'
    >>> test.socket.respond_200(url, body)
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    >>> this_browser.display_list #doctest: +NORMALIZE_WHITESPACE
    [DrawText(top=20.25 left=13 bottom=32.25 text=A font=Font size=12 weight=normal slant=roman style=None family=foo),
     DrawText(top=20.25 left=37 bottom=32.25 text=B font=Font size=12 weight=normal slant=roman style=None family=bar)]
