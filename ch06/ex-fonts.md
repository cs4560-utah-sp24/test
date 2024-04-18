Tests for WBE Chapter 6 Exercise `Fonts`
========================================

Implement the `font-family` property, an inheritable property that
names which font should be used in an element. Make code fonts use
some nice monospaced font like `Courier`.

The default font should be `Times` and the font for `<code>` elements
`Courier`. Make sure it's possible to inherit and override
`font-family`.

Please modify the `__repr__` method of your `DrawText` class to print
the font. Specifically, modify it as such:

```
class DrawText:
    def __repr__(self):
        return "DrawText(top={} left={} bottom={} text={} font={})" \
            .format(self.top, self.left, self.bottom, self.text, self.font)
```

These tests need that to make sure you're using the right font.

Tests
-----

We'll define a little helper function to test styles:

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> wbemocks.NORMALIZE_FONT = False
    >>> import browser
    >>> def print_font_style(style):
    ...     for key in sorted(style):
    ...         if key == "vertical-align": continue
    ...         if key == "font-variant": continue
    ...         val = style[key]
    ...         print(f"{key}: {val}")

The default font-family should be "Times".

    >>> html = browser.Element("html", {}, None)
    >>> body = browser.Element("body", {}, html)
    >>> div = browser.Element("div", {}, body)
    >>> browser.style(html, [])
    >>> print_font_style(html.style)
    color: black
    font-family: Times
    font-size: 16px
    font-style: normal
    font-weight: normal

The font for `code` elements should be "Courier".

    >>> content = "<code>code</code>"
    >>> url = browser.URL(wbemocks.socket.serve(content))
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    >>> this_browser.display_list
    [DrawText(top=20.25 left=13 bottom=32.25 text=code font=Font size=12 weight=normal slant=roman style=None family=Courier)]

Inheritance should be handled.

    >>> body = """
    ... <p style="font-family:foo">
    ... <span>A</span>
    ... <span style="font-family:bar"> B </span>
    ... </p>"""
    >>> url = browser.URL(wbemocks.socket.serve(body))
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    >>> wbemocks.print_list(this_browser.display_list)
    DrawText(top=20.25 left=13 bottom=32.25 text=A font=Font size=12 weight=normal slant=roman style=None family=foo)
    DrawText(top=20.25 left=37 bottom=32.25 text=B font=Font size=12 weight=normal slant=roman style=None family=bar)
