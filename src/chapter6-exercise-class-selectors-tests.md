Tests for WBE Chapter 6 Exercise `Class Selectors`
=======================

Description
-----------

Any HTML element can have a class attribute, whose value is a space-separated 
  list of tags that apply to that element. 
A CSS class selector, like .main, affects all elements tagged main. 
Implement class selectors; give them priority 10. 
If you’ve implemented them correctly, you should see code blocks in this book 
  being syntax-highlighted.

    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> import browser
    >>> def test_parse(css):
    ...     rules = browser.CSSParser(css).parse()
    ...     for sel, pairs in sorted(rules, key=lambda sp:sp[0].priority):
    ...         print(sel)
    ...         for key in sorted(pairs):
    ...             val = pairs[key]
    ...             print(f"  {key}: {val}")

To do this you will need to add a new class called `ClasSelector` to perform
  the matching.

    >>> browser.ClassSelector("b").matches(
    ...   browser.Element("p", {"class": "b"}, None))
    True

    >>> browser.ClassSelector("b").matches(
    ...   browser.Element("p", {"class": "a"}, None))
    False

    >>> browser.ClassSelector("b").matches(
    ...   browser.Element("p", {"class": "a b"}, None))
    True
    
    >>> browser.ClassSelector("b").matches(
    ...   browser.Element("p", {"class": "b a"}, None))
    True

    >>> browser.ClassSelector("b").matches(
    ...   browser.Element("p", {"class": "bat"}, None))
    False

This class should be used when parsing CSS.

    >>> test_parse(".main { font-size:100px ;}")
    ClassSelector(html_class=main, priority=10)
      font-size: 100px

Class selectors can also be used as part of descendant selectors.

    >>> test_parse(".a p { font-size:10px ;}")
    DescendantSelector(ancestor=ClassSelector(html_class=a, priority=10), descendant=TagSelector(tag=p, priority=1), priority=11)
      font-size: 10px

    >>> test_parse("p .a { color:blue ;}")
    DescendantSelector(ancestor=TagSelector(tag=p, priority=1), descendant=ClassSelector(html_class=a, priority=10), priority=11)
      color: blue

    >>> test_parse(".a .b { font-weight:bold ;}")
    DescendantSelector(ancestor=ClassSelector(html_class=a, priority=10), descendant=ClassSelector(html_class=b, priority=10), priority=20)
      font-weight: bold

Selector priority should be correct.
The `test_parse` function sorts by priority.

    >>> test_parse("h1 b { color:orange ;}"
    ...          + ".foo { color:yellow ;}"
    ...          + "p { color:red ;}"
    ...          + " .foo p { color:green ;}")
    TagSelector(tag=p, priority=1)
      color: red
    DescendantSelector(ancestor=TagSelector(tag=h1, priority=1), descendant=TagSelector(tag=b, priority=1), priority=2)
      color: orange
    ClassSelector(html_class=foo, priority=10)
      color: yellow
    DescendantSelector(ancestor=ClassSelector(html_class=foo, priority=10), descendant=TagSelector(tag=p, priority=1), priority=11)
      color: green

