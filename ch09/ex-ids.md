Tests for WBE Chapter 9 Exercise `IDs`
============================================

    When an HTML element has an `id` attribute, a JavaScript variable
pointing to that element is predefined. So, if a page has a `<div
id="foo"></div>`, then there’s a variable `foo` referring to that
node. Implement this in your browser. Make sure to handle the case of
nodes being added and removed (such as with `innerHTML`).

You can assume that element `id`s are always valid JS identifiers and
that ids will not collide. You don't have to (but can if you'd like)
support adding and removing elements through other APIs your browser
supports.

Tests
-----

Boilerplate.

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> import browser

Create the site to wbemocks.

    >>> url = wbemocks.socket.serve("<div id=alice><div>")
    >>> this_browser = browser.Browser()
    >>> this_browser.new_tab(browser.URL(url))
    >>> js = this_browser.active_tab.js

Check that the id from the page was added to the js environment.

    >>> js.run("alice;")
    {'handle': 0}
    >>> browser.print_tree(this_browser.active_tab.nodes)
     <html>
       <body>
         <div id="alice">
           <div>

Modify the page but do not add an id.

    >>> js.run("void(alice.innerHTML" +
    ...        " = '<b>No</b> new ids added')")
    >>> js.run("alice;")
    {'handle': 0}
    >>> browser.print_tree(this_browser.active_tab.nodes)
     <html>
       <body>
         <div id="alice">
           <b>
             'No'
           ' new ids added'

Replace that content with something that has an id.

    >>> js.run("void(alice.innerHTML" +
    ...        " = '<b id=one>One</b> new id added')")
    >>> js.run("alice;")
    {'handle': 0}
    >>> js.run("one;")
    {'handle': 1}
    >>> browser.print_tree(this_browser.active_tab.nodes)
     <html>
       <body>
         <div id="alice">
           <b id="one">
             'One'
           ' new id added'


Replace the id with something that has a different id.

    >>> js.run("void(alice.innerHTML" +
    ...        " = '<p id=replacement>Id was replaced</p>')")
    >>> js.run("alice;")
    {'handle': 0}
    >>> js.run("one;")
    Traceback (most recent call last):
      ...
    _dukpy.JSRuntimeError: ReferenceError: identifier 'one' undefined
        at [anon] (duk_js_var.c:1239) internal
        at eval (eval:1) preventsyield
    >>> js.run("replacement;")
    {'handle': 2}
    >>> browser.print_tree(this_browser.active_tab.nodes)
     <html>
       <body>
         <div id="alice">
           <p id="replacement">
             'Id was replaced'

Empty the document of ids.

    >>> js.run("void(document.querySelectorAll('body')[0].innerHTML" +
    ...        " = 'No ids')")
    >>> js.run("alice;")
    Traceback (most recent call last):
      ...
    _dukpy.JSRuntimeError: ReferenceError: identifier 'alice' undefined
        at [anon] (duk_js_var.c:1239) internal
        at eval (eval:1) preventsyield
    >>> js.run("one;")
    Traceback (most recent call last):
      ...
    _dukpy.JSRuntimeError: ReferenceError: identifier 'one' undefined
        at [anon] (duk_js_var.c:1239) internal
        at eval (eval:1) preventsyield
    >>> js.run("replacement;")
    Traceback (most recent call last):
      ...
    _dukpy.JSRuntimeError: ReferenceError: identifier 'replacement' undefined
        at [anon] (duk_js_var.c:1239) internal
        at eval (eval:1) preventsyield
    >>> browser.print_tree(this_browser.active_tab.nodes)
     <html>
       <body>
         'No ids'





Create the site with an element with ID "alice"

    >>> url = wbemocks.socket.serve("<div id=outer><div id=alice>Content</div></div>")
    >>> this_browser = browser.Browser()
    >>> this_browser.new_tab(browser.URL(url))
    >>> js = this_browser.active_tab.js

Check initial binding for "alice"

    >>> js.run("alice;")
    {'handle': 1}
    >>> browser.print_tree(this_browser.active_tab.nodes)
     <html>
       <body>
         <div id="outer">
           <div id="alice">
             'Content'

Modify content without changing ID

    >>> js.run("void(alice.innerHTML = '<b>Modified Content</b>')")

Check binding for "alice" again (should still be valid)

    >>> js.run("alice;")
    {'handle': 1}
    >>> browser.print_tree(this_browser.active_tab.nodes)
     <html>
       <body>
         <div id="outer">
           <div id="alice">
             <b>
               'Modified Content'


Modify content and add a new element with the same ID "alice"

    >>> js.run("void(outer.innerHTML = '<div id=\"alice\">Replaced Content</div>')")

Check binding for the new element with ID "alice"

    >>> js.run("alice;")
    {'handle': 2}
    >>> browser.print_tree(this_browser.active_tab.nodes)
     <html>
       <body>
         <div id="outer">
           <div id="alice">
             'Replaced Content'


Test: Add nodes more deeply nested than the top-level of the `innerHTML` string

    >>> url = wbemocks.socket.serve("<div id='outer'><div id='inner'></div></div>")
    >>> this_browser = browser.Browser()
    >>> this_browser.new_tab(browser.URL(url))
    >>> js = this_browser.active_tab.js

    >>> js.run("outer;")
    {'handle': 0}
    >>> browser.print_tree(this_browser.active_tab.nodes)
     <html>
       <body>
         <div id="outer">
           <div id="inner">
    >>> js.run("inner;")
    {'handle': 1}

