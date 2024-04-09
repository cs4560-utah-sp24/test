Tests for WBE Chapter 4 Exercise `Paragraphs`
=============================================

It’s not clear what it would mean for one paragraph to contain
another. Change the parser so that a document like
`<p>hello<p>world</p>` results in two sibling paragraphs instead of
one paragraph inside another; real browsers do this too. 

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
			 
			 
Test when <p> tags have different attributes from each other			 
	>>> test_parse("<p class='first-paragraph'>This has a class</p><p id='second-paragraph'>This has an ID</p>")
     <html>
       <body>
         <p class="first-paragraph">
           'This has a class'
         <p id="second-paragraph">
           'This has an ID'
		 
		 
 Test that parent pointers are set correctly	 
	>>> test_parse("<div><p>Paragraph within a div</p><b>Bold text</b></div>")
     <html>
       <body>
         <div>
           <p>
             'Paragraph within a div'
           <b>
             'Bold text'

