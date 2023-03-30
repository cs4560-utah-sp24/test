Tests for WBE Chapter 4 Exercise `Scripts`
==========================================

Description
------------

Scripts: JavaScript code embedded in a `<script>` tag uses the left angle 
  bracket to mean less-than. 
Modify your lexer so that the contents of `<script>` tags are treated 
  specially: no tags are allowed inside `<script>`, except the `</script>` 
  close tag.

Testing boilerplate:

    >>> import browser
    >>> def test_parse(text):
    ...     parser = browser.HTMLParser(text)
    ...     browser.print_tree(parser.parse())


Scripts should be able to contain singular less than or greater than signs.

    >>> test_parse("<script> a < b </script>")
     <html>
       <head>
         <script>
           ' a < b '

    >>> test_parse("<script> a > b </script>")
     <html>
       <head>
         <script>
           ' a > b '

Similarly, HTML tags in a script should just be considered part of the text 
  node.

    >>> test_parse("<script> <br> <body> </head> </script>")
     <html>
       <head>
         <script>
           ' <br> <body> </head> '

The script should end only with a complete end script tag.

    >>> test_parse("<script> <script> </script>")
     <html>
       <head>
         <script>
           ' <script> '

    >>> test_parse("<script> /script> </script>")
     <html>
       <head>
         <script>
           ' /script> '

    >>> test_parse("<script> </scriptfoo </script>")
     <html>
       <head>
         <script>
           ' </scriptfoo '

    >>> test_parse('<script> "</scri" "pt>" </script>')
     <html>
       <head>
         <script>
           ' "</scri" "pt>" '
