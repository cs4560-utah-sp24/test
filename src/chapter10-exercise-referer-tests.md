Tests for WBE Chapter 10 Exercise `Referer`
============================================

Description
-----------
When your browser visits a web page, or when it loads a CSS or JavaScript file,
    it sends a Referer header (Yep, spelled that way.) containing the URL it is
    coming from.
Sites often use this for analytics.
Implement this in your browser.
However, some URLs contain personal data that they don’t want revealed to other
    websites, so browsers support a Referrer-Policy header, which can contain
    values like no-referer (never send the Referer header when leaving this
    page) or same-origin (only do so if navigating to another page on the same
    origin). Implement those two values for Referer-Policy.


Extra Requirements
------------------
* Note the difference in spelling, the headers are `Referer` and
  `Referrer-Policy`.



Test code
---------

Boilerplate.

    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> test.NO_CACHE = True
    >>> test.NORMALIZE_FONT = True
    >>> import browser


Load a page with some CSS, and check that `Referer` is used.

    >>> url = "http://test.test.chapter10-referer-1/"
    >>> body = """<!DOCTYPE html>
    ... <link rel="stylesheet" href="style.css" />
    ... Empty"""
    >>> test.socket.respond_ok(url, body)
    >>> test.socket.respond_ok(url + "style.css", "")
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    >>> req = test.socket.last_request(url + "style.css").decode().lower()
    >>> "referer:" in req
    True
    >>> "referer: {}".format(url) in req
    True

Now load a page setting the `Referrer-Policy` header to `no-referrer`, and
    check that `Referer` is not used.

    >>> url = "http://test.test.chapter10-referer-2/"
    >>> body = """<!DOCTYPE html>
    ... <script src=http://test.test.chapter10-referer-2/same.js></script>
    ... <script src=http://test.diff.chapter10-referer-2/diff.js></script>
    ... Empty"""
    >>> body = b"HTTP/1.0 200 OK\r\nReferrer-Policy: no-referrer\r\n\r\n" + body.encode("utf8")
    >>> test.socket.respond(url, body)
    >>> test.socket.respond_ok("http://test.test.chapter10-referer-2/same.js", "")
    >>> test.socket.respond_ok("http://test.diff.chapter10-referer-2/diff.js", "")
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    >>> req = test.socket.last_request("http://test.test.chapter10-referer-2/same.js").decode().lower()
    >>> "referer:" in req
    False
    >>> req = test.socket.last_request("http://test.diff.chapter10-referer-2/diff.js").decode().lower()
    >>> "referer:" in req
    False

Finally load a page setting the `Referrer-Policy` header to `same-origin`, and
    check that `Referer` is only used when the origin is the same.


    >>> url = "http://test.test.chapter10-referer-3/"
    >>> body = """<!DOCTYPE html>
    ... <script src=http://test.test.chapter10-referer-3/same.js></script>
    ... <script src=http://test.diff.chapter10-referer-3/diff.js></script>
    ... Empty"""
    >>> body = b"HTTP/1.0 200 OK\r\nReferrer-Policy: same-origin\r\n\r\n" + body.encode("utf8")
    >>> test.socket.respond(url, body)
    >>> test.socket.respond_ok("http://test.test.chapter10-referer-3/same.js", "")
    >>> test.socket.respond_ok("http://test.diff.chapter10-referer-3/diff.js", "")
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    >>> req = test.socket.last_request("http://test.test.chapter10-referer-3/same.js").decode().lower()
    >>> "referer:" in req
    True
    >>> "referer: {}".format(url) in req
    True
    >>> req = test.socket.last_request("http://test.diff.chapter10-referer-3/diff.js").decode().lower()
    >>> "referer:" in req
    False

