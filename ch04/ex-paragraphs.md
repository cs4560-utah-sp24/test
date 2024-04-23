Tests for WBE Chapter 4 Exercise `Paragraphs`
=============================================

It’s not clear what it would mean for one paragraph to contain
another. Change the parser so that a document like
`<p>hello<p>world</p>` results in two sibling paragraphs instead of
one paragraph inside another; real browsers do this too. ~~Do the same
for `<li>` elements, but make sure nested lists are still possible.~~

Make sure to handle cases like `<p><b><p>`. In this case, all tags
inside the first paragraph should be closed and then re-opened in the
second paragraph.


Description
------------

Testing boilerplate:

    >>> import wbemocks
    >>> import browser
    >>> def test_parse(text):
    ...     parser = browser.HTMLParser(text)
    ...     browser.print_tree(parser.parse())

These two should result in the same parse tree.

    >>> test_parse("<p>hello</p><p>world</p>")
     <html>
       <body>
         <p>
           'hello'
         <p>
           'world'

    >>> test_parse("<p>hello<p>world</p></p>")
     <html>
       <body>
         <p>
           'hello'
         <p>
           'world'


Any tags that are open when encountering the second paragraph should be closed
  with the first paragraph, but also reopened and applied to the second.

    >>> test_parse("<p><b>hello<p>world</b></p></p>")
     <html>
       <body>
         <p>
           <b>
             'hello'
         <p>
           <b>
             'world'





Test when `<p>` tags have different attributes from each other

    >>> body = """
    ... <p style="font-family:foo">
    ... A
    ... <p class="diff">
    ... B
    ... """
    >>> test_parse(body)
     <html>
       <body>
         <p style="font-family:foo">
           '\nA\n'
         <p class="diff">
           '\nB\n'


Test that parent pointers are set correctly

    >>> test_parse("<p>This is <b>paragraph one</b> with <p>nested paragraph two</p></p>")
     <html>
       <body>
         <p>
           'This is '
           <b>
             'paragraph one'
           ' with '
         <p>
           'nested paragraph two'
