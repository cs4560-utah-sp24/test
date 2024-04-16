Tests for WBE Chapter 10 Exercise `Referer`
===========================================

When your browser visits a web page, or when it loads a CSS or
JavaScript file, it sends a `Referer` header (yep, spelled that way)
containing the URL it is coming from. Sites often use this for
analytics. Implement this in your browser. However, some URLs contain
personal data that they don’t want revealed to other websites, so
browsers support a `Referrer-Policy` header, which can contain values
like `no-referrer` (never send the `Referer` header when leaving this
page) or `same-origin` (only do so if navigating to another page on
the same origin). Implement those two values for `Referrer-Policy`.

Note the differences in spelling, the headers are `Referer` and
`Referrer-Policy`, and the value is `no-referrer`. You can blame
[Phillip Hallam-Baker][wiki-referer]

[wiki-referer]: https://en.wikipedia.org/wiki/HTTP_referer#Etymology


Tests
-----

Boilerplate.

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> wbemocks.NO_CACHE = True
    >>> import browser

Load a page with some CSS, and check that `Referer` is used.

    >>> url = "http://wbemocks.wbemocks.chapter10-referer-1/"
    >>> body = """<!DOCTYPE html>
    ... <link rel="stylesheet" href="style.css" />
    ... Empty"""
    >>> wbemocks.socket.respond_ok(url, body)
    >>> wbemocks.socket.respond_ok(url + "style.css", "")
    >>> this_browser = browser.Browser()
    >>> this_browser.new_tab(browser.URL(url))
    >>> req = wbemocks.socket.last_request(url + "style.css").decode().lower()
    >>> "referer:" in req
    True
    >>> "referer: {}".format(url) in req
    True

Now load a page setting the `Referrer-Policy` header to `no-referrer`, and
    check that `Referer` is not used.

    >>> url = "http://wbemocks.wbemocks.chapter10-referer-2/"
    >>> body = """<!DOCTYPE html>
    ... <script src=http://wbemocks.wbemocks.chapter10-referer-2/same.js></script>
    ... <script src=http://wbemocks.diff.chapter10-referer-2/diff.js></script>
    ... Empty"""
    >>> body = b"HTTP/1.0 200 OK\r\nReferrer-Policy: no-referrer\r\n\r\n" + body.encode("utf8")
    >>> wbemocks.socket.respond(url, body)
    >>> wbemocks.socket.respond_ok("http://wbemocks.wbemocks.chapter10-referer-2/same.js", "")
    >>> wbemocks.socket.respond_ok("http://wbemocks.diff.chapter10-referer-2/diff.js", "")
    >>> this_browser = browser.Browser()
    >>> this_browser.new_tab(browser.URL(url))
    >>> req = wbemocks.socket.last_request("http://wbemocks.wbemocks.chapter10-referer-2/same.js").decode().lower()
    >>> "referer:" in req
    False
    >>> req = wbemocks.socket.last_request("http://wbemocks.diff.chapter10-referer-2/diff.js").decode().lower()
    >>> "referer:" in req
    False

Finally load a page setting the `Referrer-Policy` header to `same-origin`, and
    check that `Referer` is only used when the origin is the same.


    >>> url = "http://wbemocks.wbemocks.chapter10-referer-3/"
    >>> body = """<!DOCTYPE html>
    ... <script src=http://wbemocks.wbemocks.chapter10-referer-3/same.js></script>
    ... <script src=http://wbemocks.diff.chapter10-referer-3/diff.js></script>
    ... Empty"""
    >>> body = b"HTTP/1.0 200 OK\r\nReferrer-Policy: same-origin\r\n\r\n" + body.encode("utf8")
    >>> wbemocks.socket.respond(url, body)
    >>> wbemocks.socket.respond_ok("http://wbemocks.wbemocks.chapter10-referer-3/same.js", "")
    >>> wbemocks.socket.respond_ok("http://wbemocks.diff.chapter10-referer-3/diff.js", "")
    >>> this_browser = browser.Browser()
    >>> this_browser.new_tab(browser.URL(url))
    >>> req = wbemocks.socket.last_request("http://wbemocks.wbemocks.chapter10-referer-3/same.js").decode().lower()
    >>> "referer:" in req
    True
    >>> "referer: {}".format(url) in req
    True
    >>> req = wbemocks.socket.last_request("http://wbemocks.diff.chapter10-referer-3/diff.js").decode().lower()
    >>> "referer:" in req
    False

