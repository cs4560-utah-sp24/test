Tests for WBE Chapter 4 Exercise `Comments`
===========================================

Description
------------

Update the HTML lexer to support comments. Comments in HTML begin with `<!--` 
  and end with `-->`.
However, comments aren’t the same as tags: they can contain any text, including
  left and right angle brackets.
The lexer should skip comments, not generating any token at all.
Check: is `<!-->` a comment, or does it just start one?


Testing boilerplate:

    >>> import test 
    >>> import browser
    >>> def test_parse(text):
    ...     parser = browser.HTMLParser(text)
    ...     browser.print_tree(parser.parse())


Comments are already partially supported by the browser.
All these should pass without changing your code.

    >>> test_parse("Lorem <!-- comment -->")
     <html>
       <body>
         'Lorem '

    >>> test_parse("<!-- comment --> ipsum")
     <html>
       <body>
         ' ipsum'

    >>> test_parse("dolor<!-- comment --> sit")
     <html>
       <body>
         'dolor'
         ' sit'

What is not yet supported are comments containing less than or greater than
  signs.

    >>> test_parse("amet <!-- <  -->")
     <html>
       <body>
         'amet '

    >>> test_parse("<!-- > -->consectetur")
     <html>
       <body>
         'consectetur'

    >>> test_parse("adipiscing <!-- <> >< --> elit")
     <html>
       <body>
         'adipiscing '
         ' elit'

This allows HTML to be commented-out.

    >>> test_parse("sed<!-- <h1>Hi</h1> -->")
     <html>
       <body>
         'sed'

There are some edge cases to take care of.

    >>> test_parse("a<!-->foo")
     <html>
       <body>
         'a'
    
    >>> test_parse("b<!--->bar")
     <html>
       <body>
         'b'

    >>> test_parse("<!---->baz")
     <html>
       <body>
         'baz'

    >>> test_parse("c<!-- foo ->-> bar --thing")
     <html>
       <body>
         'c'

    >>> test_parse("<!-- foo ->-> bar -->thing")
     <html>
       <body>
         'thing'
