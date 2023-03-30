Tests for WBE Chapter 4 Exercise `Quoted attributes`
====================================================

Description
------------

Quoted attributes can contain spaces and right angle brackets. 
Fix the lexer so that this is supported properly.
Hint: the current lexer is a finite state machine, with two states 
  (determined by in_tag). You’ll need more states.

Testing boilerplate:

    >>> import test
    >>> import browser
    >>> def test_parse(text):
    ...     parser = browser.HTMLParser(text)
    ...     browser.print_tree(parser.parse())

Quotes should already be supported, since `get_attributes` already checks for
  single and double quotes.
The issue when adding spaces to an attribute is how the text is split into 
  parts in that method.

    >>> test_parse("<img src=lhc.jpg alt='Les Horribles Cernettes'>")
     <html>
       <body>
         <img src="lhc.jpg" alt="Les Horribles Cernettes">

    >>> test_parse('<div foo="bar baz"></div>')
     <html>
       <body>
         <div foo="bar baz">

    >>> test_parse('<h1 foo="bar\'s baz"></h1>')
     <html>
       <body>
         <h1 foo="bar's baz">

    >>> test_parse("<div a='b\"c'></div>")
     <html>
       <body>
         <div a="b"c">


Allowing the greater than symbol in a quoted attribute requires the additional 
  states mentioned in the exercise.

    >>> test_parse("<br confusing='why does a <br> have an attribute?'>")
     <html>
       <body>
         <br confusing="why does a <br> have an attribute?">

There are some edge cases that should be handled

    >>> test_parse('<div foo="asdf"bgefs>')
     <html>
       <body>
         <div foo="asdf" bgefs="">

    >>> test_parse('<div =foo>')
     <html>
       <body>
         <div =foo="">

    >>> test_parse('<div=foo>')
     <html>
       <body>
         <div=foo>

    >>> test_parse('<div =foo=bar>')
     <html>
       <body>
         <div =foo="bar">

    >>> test_parse('<div a=b=c>')
     <html>
       <body>
         <div a="b=c">
