Tests for WBE Chapter 9 Exercise `Node.children`
============================================

Description
-----------

Add support for the children property on JavaScript Nodes.
Node.children returns the immediate Element children of a node, as an array.
Text children are not included.


Test code
---------

Boilerplate.

    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> import browser

Setup page and grab the javascript runtime.

    >>> url = 'http://test.test/chapter9-children/html'
    >>> page = """<!doctype html>
    ...   <p id=lorem>Lorem</p>
    ...   <p class=ipsum>Ipsum</p>"""
    >>> test.socket.respond_200(url, body=page)
    >>> b = browser.Browser()
    >>> b.load(url)
    >>> js = b.tabs[0].js


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
