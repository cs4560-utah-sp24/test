Tests for WBE Chapter 6
=======================

Chapter 6 (Applying User Styles) introduces a CSS parser for the style attribute
and style sheets, and adds support for inherited properties, tag selectors, and
descendant selectors.

    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> import browser

    >>> url = 'http://test.test/chapter6_example1'
    >>> test.socket.respond(url, b"HTTP/1.0 200 OK\r\n" +
    ... b"Header1: Value1\r\n\r\n" +
    ... b"<div>Test</div>")

Testing resolve_url
===================

    >>> browser.resolve_url("http://foo.com", "http://bar.com/")
    'http://foo.com'

    >>> browser.resolve_url("/url", "http://bar.com/")
    'http://bar.com/url'

    >>> browser.resolve_url("url2", "http://bar.com/url1")
    'http://bar.com/url2'

    >>> browser.resolve_url("url2", "http://bar.com/url1/")
    'http://bar.com/url1/url2'

Testing tree_to_list
====================

    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    >>> browser.print_tree(this_browser.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=15.0)
         BlockLayout(x=13, y=18, width=774, height=15.0)
           InlineLayout(x=13, y=18, width=774, height=15.0)
    >>> list = []
    >>> retval = browser.tree_to_list(this_browser.document, list)
    >>> retval #doctest: +NORMALIZE_WHITESPACE
    [DocumentLayout(),
     BlockLayout(x=13, y=18, width=774, height=15.0),
     BlockLayout(x=13, y=18, width=774, height=15.0),
     InlineLayout(x=13, y=18, width=774, height=15.0)]
    >>> retval == list
    True

Testing CSSParser
=================

A tag selector stores its tag, the key-value pair, and a priority of 1.

    >>> browser.CSSParser("div { foo: bar }").parse()
    [(TagSelector(tag=div, priority=1), {'foo': 'bar'})]

A descendant selector stores its ancestor and descendant as TagSelectors,
with a priority that sums them.

    >>> browser.CSSParser("div span { foo: bar }").parse()
    [(DescendantSelector(ancestor=TagSelector(tag=div, priority=1), descendant=TagSelector(tag=span, priority=1), priority=2), {'foo': 'bar'})]

    >>> browser.CSSParser("div span h1 { foo: bar }").parse()
    [(DescendantSelector(ancestor=DescendantSelector(ancestor=TagSelector(tag=div, priority=1), descendant=TagSelector(tag=span, priority=1), priority=2), descendant=TagSelector(tag=h1, priority=1), priority=3), {'foo': 'bar'})]

Multiple rules can be present.

    >>> browser.CSSParser("div { foo: bar } span { baz : baz2 }").parse()
    [(TagSelector(tag=div, priority=1), {'foo': 'bar'}), (TagSelector(tag=span, priority=1), {'baz': 'baz2'})]

Unknown syntaxes are ignored.

    >>> browser.CSSParser("a;").parse()
    []
    >>> browser.CSSParser("a {;}").parse()
    [(TagSelector(tag=a, priority=1), {})]
    >>> browser.CSSParser("{} a;").parse()
    []
    >>> browser.CSSParser("a { p }").parse()
    [(TagSelector(tag=a, priority=1), {})]
    >>> browser.CSSParser("a { p: v }").parse()
    [(TagSelector(tag=a, priority=1), {'p': 'v'})]
    >>> browser.CSSParser("a { p: ^ }").parse()
    [(TagSelector(tag=a, priority=1), {})]
    >>> browser.CSSParser("a { p: ; }").parse()
    [(TagSelector(tag=a, priority=1), {})]
    >>> browser.CSSParser("a { p: v; q }").parse()
    [(TagSelector(tag=a, priority=1), {'p': 'v'})]
    >>> browser.CSSParser("a { p: v; ; q: u }").parse()
    [(TagSelector(tag=a, priority=1), {'p': 'v', 'q': 'u'})]
    >>> browser.CSSParser("a { p: v; q:: u }").parse()
    [(TagSelector(tag=a, priority=1), {'p': 'v'})]

Whitespace can be present anywhere. This is an easy mistake to make
with a scannerless parser like used here:

    >>> browser.CSSParser("a {}").parse()
    [(TagSelector(tag=a, priority=1), {})]
    >>> browser.CSSParser("a{}").parse()
    [(TagSelector(tag=a, priority=1), {})]
    >>> browser.CSSParser("a{ }").parse()
    [(TagSelector(tag=a, priority=1), {})]
    >>> browser.CSSParser("a {} ").parse()
    [(TagSelector(tag=a, priority=1), {})]
    >>> browser.CSSParser("a {p:v} ").parse()
    [(TagSelector(tag=a, priority=1), {'p': 'v'})]
    >>> browser.CSSParser("a {p :v} ").parse()
    [(TagSelector(tag=a, priority=1), {'p': 'v'})]
    >>> browser.CSSParser("a { p:v} ").parse()
    [(TagSelector(tag=a, priority=1), {'p': 'v'})]
    >>> browser.CSSParser("a {p: v} ").parse()
    [(TagSelector(tag=a, priority=1), {'p': 'v'})]
    >>> browser.CSSParser("a {p:v } ").parse()
    [(TagSelector(tag=a, priority=1), {'p': 'v'})]

    

Testing compute_style
=====================

    >>> html = browser.Element("html", {}, None)
    >>> body = browser.Element("body", {}, html)
    >>> div = browser.Element("div", {}, body)

Other than `font-size`, this just returns the value:

    >>> browser.compute_style(body, "property", "value")
    'value'

Values for `font-size` ending in "px" return the value:

    >>> browser.compute_style(body, "font-size", "12px")
    '12px'

Percentage values are computed against the parent

    >>> html.style = {"font-size": "30px"}
    >>> browser.compute_style(body, "font-size", "100%")
    '30.0px'
    >>> browser.compute_style(body, "font-size", "80%")
    '24.0px'

    >>> body.style = {"font-size": "10px"}
    >>> browser.compute_style(div, "font-size", "100%")
    '10.0px'
    >>> browser.compute_style(div, "font-size", "80%")
    '8.0px'

Testing style
=============

    >>> html = browser.Element("html", {}, None)
    >>> body = browser.Element("body", {}, html)
    >>> div = browser.Element("div", {}, body)
    >>> def print_style(style):
    ...     for key in sorted(style):
    ...         if key == "font-family": continue
    ...         val = style[key]
    ...         print(f"{key}: {val}")

The default styles for many elements are the same:

    >>> browser.style(html, [])
    >>> print_style(html.style)
    color: black
    font-size: 16px
    font-style: normal
    font-weight: normal

    >>> browser.style(body, [])
    >>> print_style(body.style)
    color: black
    font-size: 16px
    font-style: normal
    font-weight: normal

    >>> browser.style(div, [])
    >>> print_style(div.style)
    color: black
    font-size: 16px
    font-style: normal
    font-weight: normal

    >>> rules = browser.CSSParser(
    ... "html { font-size: 10px} body { font-size: 90% } \
    ... div { font-size: 90% } ").parse()

Percentage font sizes work as expected:

    >>> browser.style(html, rules)
    >>> print_style(html.style)
    color: black
    font-size: 10px
    font-style: normal
    font-weight: normal

    >>> browser.style(body, rules)
    >>> print_style(body.style)
    color: black
    font-size: 9.0px
    font-style: normal
    font-weight: normal

    >>> browser.style(div, rules)
    >>> print_style(div.style)
    color: black
    font-size: 8.1px
    font-style: normal
    font-weight: normal


Inherited properties work (`font-weight` is an inherited property):

    >>> rules = browser.CSSParser("html { font-weight: bold}").parse()
    >>> browser.style(html, rules)
    >>> print_style(html.style)
    color: black
    font-size: 16px
    font-style: normal
    font-weight: bold

    >>> browser.style(body, rules)
    >>> print_style(body.style)
    color: black
    font-size: 16px
    font-style: normal
    font-weight: bold

    >>> browser.style(div, rules)
    >>> print_style(div.style)
    color: black
    font-size: 16px
    font-style: normal
    font-weight: bold


Other properties do not:

    >>> rules = browser.CSSParser("html { background-color: green}").parse()
    >>> browser.style(html, rules)
    >>> print_style(html.style)
    background-color: green
    color: black
    font-size: 16px
    font-style: normal
    font-weight: normal

    >>> browser.style(body, rules)
    >>> print_style(body.style)
    color: black
    font-size: 16px
    font-style: normal
    font-weight: normal

    >>> browser.style(div, rules)
    >>> print_style(div.style)
    color: black
    font-size: 16px
    font-style: normal
    font-weight: normal


Descendant selectors work:

    >>> rules = browser.CSSParser("html div { background-color: green}").parse()
    >>> browser.style(html, rules)
    >>> print_style(html.style)
    color: black
    font-size: 16px
    font-style: normal
    font-weight: normal

    >>> browser.style(body, rules)
    >>> print_style(body.style)
    color: black
    font-size: 16px
    font-style: normal
    font-weight: normal

    >>> browser.style(div, rules)
    >>> print_style(div.style)
    background-color: green
    color: black
    font-size: 16px
    font-style: normal
    font-weight: normal


Priorities work (descendant selectors high higher priority than tag selectors):

    >>> rules = browser.CSSParser(
    ... "html div { background-color: green} div { background-color: blue").parse()
    >>> browser.style(html, rules)
    >>> print_style(html.style)
    color: black
    font-size: 16px
    font-style: normal
    font-weight: normal

    >>> browser.style(body, rules)
    >>> print_style(body.style)
    color: black
    font-size: 16px
    font-style: normal
    font-weight: normal

    >>> browser.style(div, rules)
    >>> print_style(div.style)
    background-color: green
    color: black
    font-size: 16px
    font-style: normal
    font-weight: normal

    >>> url2 = 'http://test.test/chapter6_example2'
    >>> test.socket.respond(url2, b"HTTP/1.0 200 OK\r\n" +
    ... b"Header1: Value1\r\n\r\n" +
    ... b"<div style=\"color:blue\">Test</div>")


Style attributes have the highest priority:

    >>> this_browser = browser.Browser()
    >>> this_browser.load(url2)
    >>> this_browser.document.children[0].children[0].children[0].node.style['color']
    'blue'
