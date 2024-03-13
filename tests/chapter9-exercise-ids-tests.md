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

Test code
---------

Boilerplate.

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> wbemocks.NORMALIZE_FONT = True
    >>> import browser

Create the site to wbemocks.

    >>> url = wbemocks.socket.serve("<div id=alice><div>")
    >>> this_browser = browser.Browser()
    >>> this_browser.new_tab(browser.URL(url))
    >>> js = this_browser.active_tab.js

Check that the id from the page was added to the js environment.

    >>> js.run("alice;")
    {'handle': 0}
    >>> browser.print_tree(this_browser.active_tab.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=0)
         BlockLayout(x=13, y=18, width=774, height=0)
           BlockLayout(x=13, y=18, width=774, height=0)
             BlockLayout(x=13, y=18, width=774, height=0)

Modify the page but do not add an id.

    >>> js.run("void(alice.innerHTML" +
    ...        " = '<b>No</b> new ids added')")
    >>> js.run("alice;")
    {'handle': 0}
    >>> browser.print_tree(this_browser.active_tab.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=15.0)
         BlockLayout(x=13, y=18, width=774, height=15.0)
           BlockLayout(x=13, y=18, width=774, height=15.0)
             LineLayout(x=13, y=18, width=774, height=15.0)
               TextLayout(x=13, y=20.25, width=24, height=12, word=No)
               TextLayout(x=49, y=20.25, width=36, height=12, word=new)
               TextLayout(x=97, y=20.25, width=36, height=12, word=ids)
               TextLayout(x=145, y=20.25, width=60, height=12, word=added)

Replace that content with something that has an id.

    >>> js.run("void(alice.innerHTML" +
    ...        " = '<b id=one>One</b> new id added')")
    >>> js.run("alice;")
    {'handle': 0}
    >>> js.run("one;")
    {'handle': 1}
    >>> browser.print_tree(this_browser.active_tab.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=15.0)
         BlockLayout(x=13, y=18, width=774, height=15.0)
           BlockLayout(x=13, y=18, width=774, height=15.0)
             LineLayout(x=13, y=18, width=774, height=15.0)
               TextLayout(x=13, y=20.25, width=36, height=12, word=One)
               TextLayout(x=61, y=20.25, width=36, height=12, word=new)
               TextLayout(x=109, y=20.25, width=24, height=12, word=id)
               TextLayout(x=145, y=20.25, width=60, height=12, word=added)

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
    >>> browser.print_tree(this_browser.active_tab.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=15.0)
         BlockLayout(x=13, y=18, width=774, height=15.0)
           BlockLayout(x=13, y=18, width=774, height=15.0)
             BlockLayout(x=13, y=18, width=774, height=15.0)
               LineLayout(x=13, y=18, width=774, height=15.0)
                 TextLayout(x=13, y=20.25, width=24, height=12, word=Id)
                 TextLayout(x=49, y=20.25, width=36, height=12, word=was)
                 TextLayout(x=97, y=20.25, width=96, height=12, word=replaced)

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
    >>> browser.print_tree(this_browser.active_tab.document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=15.0)
         BlockLayout(x=13, y=18, width=774, height=15.0)
           LineLayout(x=13, y=18, width=774, height=15.0)
             TextLayout(x=13, y=20.25, width=24, height=12, word=No)
             TextLayout(x=49, y=20.25, width=36, height=12, word=ids)




