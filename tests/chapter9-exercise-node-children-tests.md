Tests for WBE Chapter 9 Exercise `Node.children`
============================================

Add support for the `children` property on JavaScript `Node`s.
`Node.children` returns the immediate `Element` children of a node, as
an array. `Text` children are not included.

Tests
-----

Boilerplate.

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> import browser

Setup page and grab the javascript runtime.

    >>> page = """<!doctype html>
    ...   <p id=lorem>Lorem</p>
    ...   <p class=ipsum>Ipsum</p>"""
    >>> url = wbemocks.socket.serve(page)
    >>> b = browser.Browser()
    >>> b.new_tab(browser.URL(url))
    >>> js = b.active_tab.js

Look at the contents of the body.

    >>> js.run("void(bdy_chld = document.querySelectorAll('body')[0].children)")
    >>> js.run("bdy_chld.length")
    2
    >>> js.run("bdy_chld[0].getAttribute('id')")
    'lorem'
    >>> js.run("bdy_chld[1].getAttribute('class')")
    'ipsum'

Text children should not be included.

    >>> js.run("document.querySelectorAll('p')[0].children")
    []

    >>> js.run("document.querySelectorAll('p')[1].children")
    []
