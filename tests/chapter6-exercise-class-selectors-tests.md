Tests for WBE Chapter 6 Exercise `Class Selectors`
=======================

Any HTML element can have a class attribute, whose value is a
space-separated list of tags that apply to that element. A CSS class
selector, like `.main`, affects all elements tagged main. Implement
class selectors; give them priority 10. If you’ve implemented them
correctly, you should see code blocks in this book being
syntax-highlighted.

An element can have more than one class. Class names *are* case
sensitive, so you do not need to case fold them.

Name the selector class for class selectors `ClassSelector`. Note that
`class` is a keyword in Python, so you'll need to call the field
holding the class name `classname`. Give this class the following
`__repr__`:

```
class ClassSelector:
    def __repr__(self):
        return "ClassSelector(classname={}, priority={})".format(
            self.classname, self.priority)
```

Tests
-----

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> import browser

Define a new class called `ClassSelector` to perform the matching.

    >>> browser.ClassSelector("b").matches(
    ...   browser.Element("p", {"class": "b"}, None))
    True
    >>> browser.ClassSelector("b").matches(
    ...   browser.Element("p", {"class": "a"}, None))
    False

If an element does not have a `class`, it shouldn't match:

    >>> browser.ClassSelector("b").matches(
    ...   browser.Element("p", {}, None))
    False

Make sure it works for elements with more than one class; the `class`
attribute is a space-separated list:

    >>> browser.ClassSelector("b").matches(
    ...   browser.Element("p", {"class": "a b"}, None))
    True
    >>> browser.ClassSelector("b").matches(
    ...   browser.Element("p", {"class": "b a"}, None))
    True
    >>> browser.ClassSelector("b").matches(
    ...   browser.Element("p", {"class": "bat"}, None))
    False
    >>> browser.ClassSelector("b").matches(
    ...   browser.Element("p", {"class": ""}, None))
    False

Class selectors are case-sensitive:

    >>> browser.ClassSelector("b").matches(
    ...   browser.Element("p", {"class": "B"}, None))
    False
    >>> browser.ClassSelector("B").matches(
    ...   browser.Element("p", {"class": "b"}, None))
    False

This class should be used when parsing CSS. We'll define a helper
function to print parsed rules.

    >>> def test_parse(css):
    ...     rules = browser.CSSParser(css).parse()
    ...     for sel, pairs in sorted(rules, key=lambda sp:sp[0].priority):
    ...         print(sel)
    ...         for key in sorted(pairs):
    ...             val = pairs[key]
    ...             print(f"  {key}: {val}")
    >>> test_parse(".main { font-size:100px ;}")
    ClassSelector(classname=main, priority=10)
      font-size: 100px

Note that the class selector is case sensitive, but the tag selector
isn't:

    >>> test_parse(".main {} .MAIN {} p {} P {}")
    TagSelector(tag=p, priority=1)
    TagSelector(tag=p, priority=1)
    ClassSelector(classname=main, priority=10)
    ClassSelector(classname=MAIN, priority=10)

Class selectors can also be used as part of descendant selectors.

    >>> test_parse(".a p { font-size:10px ;}")
    DescendantSelector(ancestor=ClassSelector(classname=a, priority=10), descendant=TagSelector(tag=p, priority=1), priority=11)
      font-size: 10px
    >>> test_parse("p .a { color:blue ;}")
    DescendantSelector(ancestor=TagSelector(tag=p, priority=1), descendant=ClassSelector(classname=a, priority=10), priority=11)
      color: blue
    >>> test_parse(".a .b { font-weight:bold ;}")
    DescendantSelector(ancestor=ClassSelector(classname=a, priority=10), descendant=ClassSelector(classname=b, priority=10), priority=20)
      font-weight: bold

Selector priority should be correct. The `test_parse` function sorts
by priority.

    >>> test_parse("""
    ...   h1 b { color:orange ;}
    ...   .foo { color:yellow ;}
    ...   p { color:red ;}
    ...    .foo p { color:green ;}""")
    TagSelector(tag=p, priority=1)
      color: red
    DescendantSelector(ancestor=TagSelector(tag=h1, priority=1), descendant=TagSelector(tag=b, priority=1), priority=2)
      color: orange
    ClassSelector(classname=foo, priority=10)
      color: yellow
    DescendantSelector(ancestor=ClassSelector(classname=foo, priority=10), descendant=TagSelector(tag=p, priority=1), priority=11)
      color: green

