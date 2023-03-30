Tests fsor WBE Chapter 4
=======================

Chapter 4 (Constructing a Document Tree) adds support for the document tree
(i.e. the DOM).  This file contains tests for the additional functionality.

    >>> import test
    >>> import browser
    >>> def test_parse(text):
    ...     parser = browser.HTMLParser(text)
    ...     browser.print_tree(parser.parse())


Testing HTMLParser
==================

HTMLParser is a class whose constructor takes HTML body text as an argument, and
can parse it.

The implicit ``html` and `body` (and `head` when needed) tags are added:

	>>> test_parse("<html><body>test</body></html>")
	 <html>
	   <body>
	     'test'

Quotation marks around `Text` objects should be different depending on if
there are quotes within:

	>>> test_parse("<html><body>baker's dozen</body></html>")
	 <html>
	   <body>
	     "baker's dozen"

Missing tags are added in:

	>>> test_parse("test")
	 <html>
	   <body>
	     'test'

	>>> test_parse("<body>test")
	 <html>
	   <body>
	     'test'

Head tags are put in the head, and other tags, such as `div`, are put
in the body. Also, tags such as `base` are self-closing:

	>>> test_parse("<base><basefont></basefont><title></title><div></div>")
	 <html>
	   <head>
	     <base>
	     <basefont>
	     <title>
 	   <body>
 	     <div>

Missing end tags are added:

	>>> test_parse("<div>text")
	 <html>
	   <body>
	     <div>
	       'text'

Attributes can be set on tags:

	>>> test_parse("<div name1=value1 name2=value2>text</div")
	 <html>
	   <body>
	     <div name1="value1" name2="value2">
	       'text'
