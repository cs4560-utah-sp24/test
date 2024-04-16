Tests for WBE Chapter 9 Exercise `createElement`
============================================

The `document.createElement` method creates a new element, which can
be attached to the document with the `appendChild` and `insertBefore`
methods on `Node`s; unlike `innerHTML`, there’s no parsing involved.
Implement all three methods.

You don't have to handle edge cases; the tests only call `appendChild`
and `insertBefore` to add newly created elements with valid arguments.

Tests
-----

Boilerplate.

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> import browser

Show the page with no content changes by scripts.

    >>> js_url = wbemocks.socket.serve("")
    >>> body = "<script src=" + str(js_url) + "></script>"
    >>> body += "<div>Some content </div>  <p><b>More</b> content</p>"
    >>> html_url = wbemocks.socket.serve(body)
    >>> this_browser = browser.Browser()
    >>> this_browser.new_tab(browser.URL(html_url))

    >>> browser.print_tree(this_browser.active_tab.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=30.0, node=<html>)...
         BlockLayout(x=13, y=18, width=774, height=30.0, node=<body>)
           BlockLayout(x=13, y=18, width=774, height=15.0, node=<div>)
             LineLayout(x=13, y=18, width=774, height=15.0)
               TextLayout(x=13, y=20.25, width=48, height=12, word=Some)
               TextLayout(x=73, y=20.25, width=84, height=12, word=content)
           BlockLayout(x=13, y=33.0, width=774, height=15.0, node=<p>)
             LineLayout(x=13, y=33.0, width=774, height=15.0)
               TextLayout(x=13, y=35.25, width=48, height=12, word=More)
               TextLayout(x=73, y=35.25, width=84, height=12, word=content)

Set up the webpage and script links.
Create an input and add it as a child to the `<p>` at the end.

    >>> script = """
    ... new_elt = document.createElement("input");
    ... my_p = document.querySelectorAll('p')[0];
    ... my_p.appendChild(new_elt);
    ... """
    >>> js_url = wbemocks.socket.serve(script)
    >>> body = "<script src=" + str(js_url) + "></script>"
    >>> body += "<div>Some content </div>  <p><b>More</b> content</p>"
    >>> html_url = wbemocks.socket.serve(body)
    >>> this_browser = browser.Browser()
    >>> this_browser.new_tab(browser.URL(html_url))

    >>> browser.print_tree(this_browser.active_tab.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=30.0, node=<html>)...
         BlockLayout(x=13, y=18, width=774, height=30.0, node=<body>)
           BlockLayout(x=13, y=18, width=774, height=15.0, node=<div>)
             LineLayout(x=13, y=18, width=774, height=15.0)
               TextLayout(x=13, y=20.25, width=48, height=12, word=Some)
               TextLayout(x=73, y=20.25, width=84, height=12, word=content)
           BlockLayout(x=13, y=33.0, width=774, height=15.0, node=<p>)
             LineLayout(x=13, y=33.0, width=774, height=15.0)
               TextLayout(x=13, y=35.25, width=48, height=12, word=More)
               TextLayout(x=73, y=35.25, width=84, height=12, word=content)
               InputLayout(x=169, y=35.25, width=200, height=12, node=<input>)
               
Make sure to set the element's `parent` pointer:

    >>> body = this_browser.active_tab.nodes.children[1]
    >>> input = body.children[1].children[2]
    >>> input
    <input>
    >>> input.parent
    <p>

Create an input and add it inside the `<p>` before the `<b>`

    >>> script = """
    ... new_elt = document.createElement("input");
    ... my_p = document.querySelectorAll('p')[0];
    ... my_b = document.querySelectorAll('b')[0];
    ... my_p.insertBefore(new_elt, my_b);
    ... """
    >>> js_url = wbemocks.socket.serve(script)
    >>> body = "<script src=" + str(js_url) + "></script>"
    >>> body += "<div>Some content </div>  <p><b>More</b> content</p>"
    >>> html_url = wbemocks.socket.serve(body)
    >>> this_browser = browser.Browser()
    >>> this_browser.new_tab(browser.URL(html_url))

    >>> browser.print_tree(this_browser.active_tab.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=30.0, node=<html>)...
         BlockLayout(x=13, y=18, width=774, height=30.0, node=<body>)
           BlockLayout(x=13, y=18, width=774, height=15.0, node=<div>)
             LineLayout(x=13, y=18, width=774, height=15.0)
               TextLayout(x=13, y=20.25, width=48, height=12, word=Some)
               TextLayout(x=73, y=20.25, width=84, height=12, word=content)
           BlockLayout(x=13, y=33.0, width=774, height=15.0, node=<p>)
             LineLayout(x=13, y=33.0, width=774, height=15.0)
               InputLayout(x=13, y=35.25, width=200, height=12, node=<input>)
               TextLayout(x=225, y=35.25, width=48, height=12, word=More)
               TextLayout(x=285, y=35.25, width=84, height=12, word=content)

Create an input and add it inside the `<p>` at then end of its children
by using `insertBefore` with a reference node of null.

    >>> script = """
    ... new_elt = document.createElement("input");
    ... my_p = document.querySelectorAll('p')[0];
    ... my_p.insertBefore(new_elt, null);
    ... """
    >>> js_url = wbemocks.socket.serve(script)
    >>> body = "<script src=" + str(js_url) + "></script>"
    >>> body += "<div>Some content </div>  <p><b>More</b> content</p>"
    >>> html_url = wbemocks.socket.serve(body)
    >>> this_browser = browser.Browser()
    >>> this_browser.new_tab(browser.URL(html_url))

    >>> browser.print_tree(this_browser.active_tab.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=30.0, node=<html>)...
         BlockLayout(x=13, y=18, width=774, height=30.0, node=<body>)
           BlockLayout(x=13, y=18, width=774, height=15.0, node=<div>)
             LineLayout(x=13, y=18, width=774, height=15.0)
               TextLayout(x=13, y=20.25, width=48, height=12, word=Some)
               TextLayout(x=73, y=20.25, width=84, height=12, word=content)
           BlockLayout(x=13, y=33.0, width=774, height=15.0, node=<p>)
             LineLayout(x=13, y=33.0, width=774, height=15.0)
               TextLayout(x=13, y=35.25, width=48, height=12, word=More)
               TextLayout(x=73, y=35.25, width=84, height=12, word=content)
               InputLayout(x=169, y=35.25, width=200, height=12, node=<input>)
