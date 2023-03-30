Tests for WBE Chapter 10 Exercise `Certificate errors`
============================================

Description
-----------
When accessing an HTTPS page, the web server can send an invalid certificate
    (badssl.com hosts various invalid certificates you can use for testing).
In this case, the wrap_socket function will raise a certificate error;
    Catch these errors and show a warning message to the user.
For all other HTTPS pages draw a padlock (spelled \N{lock}) in the address bar.


Extra Requirements
------------------
* If you first connect your socket then wrap it the exception will be thrown when
  calling wrap_socket. If you wrap the socket before calling connect then the
  exception is thrown when calling connect.
* For the warning message to the user simply do not load the page and instead
  display the following webpage:
  ```html
  <!doctype html>
  Secure Connection Failed
  ```


Test code
---------

Boilerplate.

    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> test.NO_CACHE = True
    >>> test.NORMALIZE_FONT = True
    >>> import browser

Check that using http does not add the lock character.

    >>> test.TK_CANVAS_CALLS = list()
    >>> url = "http://test.test.chapter10-certificate-errors/"
    >>> test.socket.respond_ok(url, "Insecure page")
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    >>> tk_text = [c for c  in test.TK_CANVAS_CALLS if
    ...            c.startswith("create_text")]
    >>> any("\N{lock}" in c for c in tk_text)
    False


The lock character should be displayed when the page is https and no errors
    occur.

    >>> test.TK_CANVAS_CALLS = list()
    >>> url = "https://test.test.chapter10-certificate-errors/"
    >>> test.socket.respond_ok(url, "Secure page")
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    >>> tk_text = [c for c  in test.TK_CANVAS_CALLS if
    ...            c.startswith("create_text")]
    >>> any("\N{lock}" in c for c in tk_text)
    True


When the certificate is invalid display the above page and do not display a
    lock.

    >>> test.TK_CANVAS_CALLS = list()
    >>> this_browser = browser.Browser()
    >>> this_browser.load("https://untrusted-root.badssl.com/")
    >>> browser.print_tree(this_browser.tabs[0].document)
     DocumentLayout()
       BlockLayout(x=13, y=18, width=774, height=15.0)
         InlineLayout(x=13, y=18, width=774, height=15.0)
           LineLayout(x=13, y=18, width=774, height=15.0)
             TextLayout(x=13, y=20.25, width=72, height=12, font=Font size=12 weight=normal slant=roman style=None)
             TextLayout(x=97, y=20.25, width=120, height=12, font=Font size=12 weight=normal slant=roman style=None)
             TextLayout(x=229, y=20.25, width=72, height=12, font=Font size=12 weight=normal slant=roman style=None)

    >>> tk_text = [c for c  in test.TK_CANVAS_CALLS if
    ...            c.startswith("create_text")]
    >>> any("\N{lock}" in c for c in tk_text)
    False

