Tests for WBE Chapter 10
========================

Chapter 10 (Keeping Data Private) introduces cookies.

    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> test.NO_CACHE = True
    >>> import browser

Testing basic cookies
=====================

When a server sends a `Set-Cookie` header, the browser should save it
in the cookie jar:

    >>> this_browser = browser.Browser()
    >>> url = 'http://test.test.chapter10/login'
    >>> test.socket.respond(url, b"HTTP/1.0 200 OK\r\nSet-Cookie: foo=bar\r\n\r\nempty")
    >>> this_browser.load(url)
    >>> browser.COOKIE_JAR["test.test.chapter10"]
    ('foo=bar', {})

Moreover, the browser should now send a `Cookie` header with future
requests:

    >>> url2 = 'http://test.test.chapter10/'
    >>> test.socket.respond(url2, b"HTTP/1.0 200 OK\r\n\r\n\r\nempty")
    >>> this_browser.load(url2)
    >>> b'cookie: foo=bar' in test.socket.last_request(url2).lower()
    True

Unrelated sites should not be sent the cookie:

    >>> url3 = 'http://other.site.chapter10/'
    >>> test.socket.respond(url3, b"HTTP/1.0 200 OK\r\n\r\n\r\nempty")
    >>> this_browser.load(url3)
    >>> b'cookie' in test.socket.last_request(url3).lower()
    False

Note that these three requests were across three different tabs. All
tabs should use the same cookie jar.

Cookie values can be updated:

    >>> browser.COOKIE_JAR["test.test.chapter10"]
    ('foo=bar', {})
    >>> test.socket.respond(url, b"HTTP/1.0 200 OK\r\nSet-Cookie: foo=baz\r\n\r\nempty")
    >>> this_browser.load(url)
    >>> browser.COOKIE_JAR["test.test.chapter10"]
    ('foo=baz', {})

Testing XMLHttpRequest
======================

First, let's test the basic `XMLHttpRequest` functionality. We'll be
making a lot of `XMLHttpRequest` calls so let's add a little helper
for that:

    >>> def xhrjs(url):
    ...     return """x = new XMLHttpRequest();
    ... x.open("GET", """ + repr(url) + """, false);
    ... x.send();
    ... console.log(x.responseText);"""

Now let's test a simple same-site request:

    >>> url = "http://about.blank.chapter10/"
    >>> test.socket.respond(url, b"HTTP/1.0 200 OK\r\n\r\nempty")
    >>> url2 = "http://about.blank.chapter10/hello"
    >>> test.socket.respond(url2, b"HTTP/1.0 200 OK\r\n\r\nHello!")
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    >>> tab = this_browser.tabs[0]
    >>> tab.js.run(xhrjs(url2))
    Hello!

Relative URLs also work:

    >>> tab.js.run(xhrjs("/hello"))
    Hello!

Non-synchronous XHRs should fail:

    >>> tab.js.run("XMLHttpRequest().open('GET', '/', true)") #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    _dukpy.JSRuntimeError: <complicated error message>

If cookies are present, they should be sent:

    >>> browser.COOKIE_JAR["about.blank.chapter10"] = ('foo=bar', {})
    >>> tab.js.run(xhrjs(url2))
    Hello!
    >>> b'cookie: foo=bar' in test.socket.last_request(url2).lower()
    True

Note that the cookie value is sent.

Now let's see that cross-domain requests fail:

    >>> url3 = "http://other.site.chapter10/"
    >>> test.socket.respond(url3, b"HTTP/1.0 200 OK\r\n\r\nPrivate")
    >>> tab.js.run(xhrjs(url3)) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    _dukpy.JSRuntimeError: <complicated error message>

It's not important whether the request is _ever_ sent; the CORS
exercise requires sending it but the standard implementation does not
send it.

Testing SameSite cookies and CSRF
=================================

`SameSite` cookies should be sent on cross-site `GET`s and
same-site `POST`s but not on cross-site `POST`s.

Cookie without `SameSite` have already been tested above. Let's create
a `SameSite` cookie to start.

    >>> url = "http://test.test.chapter10/"
    >>> test.socket.respond(url, b"HTTP/1.0 200 OK\r\nSet-Cookie: bar=baz; SameSite=Lax\r\n\r\nempty")
    >>> tab.load(url)
    >>> browser.COOKIE_JAR["test.test.chapter10"]
    ('bar=baz', {'samesite': 'lax'})

Now the browser should have `bar=baz` as a `SameSite` cookie for
`test.test.chapter10`. First, let's check that it's sent in a same-site `GET`
request:

    >>> url2 = "http://test.test.chapter10/2"
    >>> test.socket.respond(url2, b"HTTP/1.0 200 OK\r\n\r\n2")
    >>> tab.load(url2)
    >>> b'cookie: bar=baz' in test.socket.last_request(url2).lower()
    True


Now let's submit a same-site `POST` and check that it's also sent
there:

    >>> url3 = "http://test.test.chapter10/add"
    >>> test.socket.respond(url3, b"HTTP/1.0 200 OK\r\n\r\nAdded!", method="POST")
    >>> tab.load(url3, body="who=me")
    >>> req = test.socket.last_request(url3).lower()
    >>> req.startswith(b'post')
    True
    >>> b'cookie: bar=baz' in req
    True
    >>> b'content-length: 6' in req
    True
    >>> req.endswith(b'who=me')
    True

Now we navigate to another site, navigate back by `GET`, and the
cookie should *still* be sent:

    >>> url4 = "http://other.site.chapter10/"
    >>> test.socket.respond(url4, b"HTTP/1.0 200 OK\r\n\r\nHi!")
    >>> tab.load(url4)
    >>> tab.load(url)
    >>> b'cookie: bar=baz' in test.socket.last_request(url).lower()
    True

Finally, let's try a cross-site `POST` request and check that in this
case the cookie is *not* sent:

    >>> tab.load(url4)
    >>> tab.load(url3, body="who=me")
    >>> req = test.socket.last_request(url3).lower()
    >>> req.startswith(b'post')
    True
    >>> b'content-length: 6' in req
    True
    >>> req.endswith(b'who=me')
    True

Testing Content-Security-Policy
===============================

We test `Content-Security-Policy` by checking that subresources are
loaded / not loaded as required. To do that we need a page with a lot
of subresources:

    >>> url = "http://test.test.chapter10/"
    >>> body = """<!doctype html>
    ... <link rel=stylesheet href=http://test.test.chapter10/css />
    ... <script src=http://test.test.chapter10/js></script>
    ... <link rel=stylesheet href=http://library.test.chapter10/css />
    ... <script src=http://library.test.chapter10/js></script>
    ... <link rel=stylesheet href=http://other.test.chapter10/css />
    ... <script src=http://other.test.chapter10/js></script>
    ... """
    >>> test.socket.respond(url, b"HTTP/1.0 200 OK\r\n\r\n" + body.encode("utf8"))

We also need to create all those subresources:

    >>> test.socket.respond_ok(url + "css", "")
    >>> test.socket.respond_ok(url + "js", "")
    >>> url2 = "http://library.test.chapter10/"
    >>> test.socket.respond_ok(url2 + "css", "")
    >>> test.socket.respond_ok(url2 + "js", "")
    >>> url3 = "http://other.test.chapter10/"
    >>> test.socket.respond_ok(url3 + "css", "")
    >>> test.socket.respond_ok(url3 + "js", "")

Now with all of these URLs set up, let's load the page without CSP and
check that all of these requests were made:

    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    >>> [test.socket.made_request(url + "css"),
    ...  test.socket.made_request(url + "js")]
    [True, True]
    >>> [test.socket.made_request(url2 + "css"),
    ...  test.socket.made_request(url2 + "js")]
    [True, True]
    >>> [test.socket.made_request(url3 + "css"),
    ...  test.socket.made_request(url3 + "js")]
    [True, True]

Now let's reload the page, but with CSP enabled for `test.test.chapter10` and
`library.test.chapter10` but not `other.test.chapter10`:

    >>> test.socket.clear_history()
    >>> test.socket.respond(url, b"HTTP/1.0 200 OK\r\n" + \
    ... b"Content-Security-Policy: default-src http://test.test.chapter10 http://library.test.chapter10\r\n\r\n" + \
    ... body.encode("utf8"))
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    Blocked script http://other.test.chapter10/js due to CSP
    Blocked style http://other.test.chapter10/css due to CSP

The URLs on `test.test.chapter10` and `library.test.chapter10` should have been loaded:

    >>> [test.socket.made_request(url + "css"),
    ...  test.socket.made_request(url + "js")]
    [True, True]
    >>> [test.socket.made_request(url2 + "css"),
    ...  test.socket.made_request(url2 + "js")]
    [True, True]

However, neither script nor style from `other.test.chapter10` should be loaded:

    >>> [test.socket.made_request(url3 + "css"),
    ...  test.socket.made_request(url3 + "js")]
    [False, False]

Let's also test that XHR is blocked by CSP. This requires a little
trickery, because cross-site XHR is already blocked, so we need a CSP
that restricts all sites---but then we can't load and run any
JavaScript!

    >>> url = "http://weird.test.chapter10/"
    >>> test.socket.respond(url, b"HTTP/1.0 200 OK\r\n" + \
    ... b"Content-Security-Policy: default-src\r\n\r\nempty")
    >>> this_browser.load(url)
    >>> tab = this_browser.tabs[-1]
    >>> tab.js.run("""
    ... x = new XMLHttpRequest()
    ... x.open('GET', 'http://weird.test.chapter10/xhr', false);
    ... x.send();""") #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      ...
    _dukpy.JSRuntimeError: <complicated wrapper around 'Cross-origin XHR blocked by CSP'>
