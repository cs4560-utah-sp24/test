Tests for WBE Chapter 9 Exercise `IDs`
============================================

Description
-----------

When an HTML element has an id attribute, a JavaScript variable pointing to
    that element is predefined.
So, if a page has a `<div id="foo"></div>`, then there’s a variable foo
    referring to that node.
Implement this in your browser.
Make sure to handle the case of nodes being added and removed (such as with
    innerHTML).


Extra Requirements
------------------
* Element ids will not collide


Test code
---------

Boilerplate.

    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> test.NORMALIZE_FONT = True
    >>> import browser

Create the site to test.

    >>> url = 'http://test.test/chapter9-ids-1/html'
    >>> html = "<div id=alice><div>"
    >>> test.socket.respond_200(url, html)
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    >>> js = this_browser.tabs[0].js

Check that the id from the page was added to the js environment.

    >>> js.run("alice;")
    {'handle': 0}
    >>> browser.print_tree(this_browser.tabs[0].document)
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
    >>> browser.print_tree(this_browser.tabs[0].document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=15.0)
         BlockLayout(x=13, y=18, width=774, height=15.0)
           InlineLayout(x=13, y=18, width=774, height=15.0)
             LineLayout(x=13, y=18, width=774, height=15.0)
               TextLayout(x=13, y=20.25, width=24, height=12, font=Font size=12 weight=bold slant=roman style=None)
               TextLayout(x=49, y=20.25, width=36, height=12, font=Font size=12 weight=normal slant=roman style=None)
               TextLayout(x=97, y=20.25, width=36, height=12, font=Font size=12 weight=normal slant=roman style=None)
               TextLayout(x=145, y=20.25, width=60, height=12, font=Font size=12 weight=normal slant=roman style=None)

Replace that content with something that has an id.

    >>> js.run("void(alice.innerHTML" +
    ...        " = '<b id=one>One</b> new id added')")
    >>> js.run("alice;")
    {'handle': 0}
    >>> js.run("one;")
    {'handle': 1}
    >>> browser.print_tree(this_browser.tabs[0].document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=15.0)
         BlockLayout(x=13, y=18, width=774, height=15.0)
           InlineLayout(x=13, y=18, width=774, height=15.0)
             LineLayout(x=13, y=18, width=774, height=15.0)
               TextLayout(x=13, y=20.25, width=36, height=12, font=Font size=12 weight=bold slant=roman style=None)
               TextLayout(x=61, y=20.25, width=36, height=12, font=Font size=12 weight=normal slant=roman style=None)
               TextLayout(x=109, y=20.25, width=24, height=12, font=Font size=12 weight=normal slant=roman style=None)
               TextLayout(x=145, y=20.25, width=60, height=12, font=Font size=12 weight=normal slant=roman style=None)

Replace the id with something that has a different id.

    >>> js.run("void(alice.innerHTML" +
    ...        " = '<p id=replacement>Id was replaced</p>')")
    >>> js.run("alice;")
    {'handle': 0}
    >>> test.errors(js.run, "one;")
    True
    >>> js.run("replacement;")
    {'handle': 2}
    >>> browser.print_tree(this_browser.tabs[0].document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=15.0)
         BlockLayout(x=13, y=18, width=774, height=15.0)
           BlockLayout(x=13, y=18, width=774, height=15.0)
             InlineLayout(x=13, y=18, width=774, height=15.0)
               LineLayout(x=13, y=18, width=774, height=15.0)
                 TextLayout(x=13, y=20.25, width=24, height=12, font=Font size=12 weight=normal slant=roman style=None)
                 TextLayout(x=49, y=20.25, width=36, height=12, font=Font size=12 weight=normal slant=roman style=None)
                 TextLayout(x=97, y=20.25, width=96, height=12, font=Font size=12 weight=normal slant=roman style=None)

Empty the document of ids.

    >>> js.run("void(document.querySelectorAll('body')[0].innerHTML" +
    ...        " = 'No ids')")
    >>> test.errors(js.run, "alice;")
    True
    >>> test.errors(js.run, "one;")
    True
    >>> test.errors(js.run, "replacement;")
    True
    >>> browser.print_tree(this_browser.tabs[0].document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=15.0)
         InlineLayout(x=13, y=18, width=774, height=15.0)
           LineLayout(x=13, y=18, width=774, height=15.0)
             TextLayout(x=13, y=20.25, width=24, height=12, font=Font size=12 weight=normal slant=roman style=None)
             TextLayout(x=49, y=20.25, width=36, height=12, font=Font size=12 weight=normal slant=roman style=None)




