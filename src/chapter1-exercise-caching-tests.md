Tests for WBE Chapter 1 Exercise `Caching`
==========================================

Testing boilerplate:

    >>> import time
    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> import browser

A server response can indicate if the response itself can be cached and for how 
  long.
The __Cache-Control__ header can be set to __max-age=[number]__ to allow caching of
  the response for __[number]__ seconds.
We can test if a browser is caching responses by changing the response and 
  telling the browser to re-request the page.

    >>> url = "http://test.test/cache_me1"
    >>> test.socket.respond(url=url, 
    ...   response=("HTTP/1.0 200 Ok\r\n" +
    ...             "Cache-Control: max-age=9001\r\n" +
    ...             "\r\n" +
    ...             "Keep this for a while").encode())
    >>> header, body = browser.request(url)
    >>> body
    'Keep this for a while'
    >>> test.socket.respond(url=url, 
    ...   response=("HTTP/1.0 200 Ok\r\n" +
    ...             "Cache-Control: max-age=9001\r\n" +
    ...             "\r\n" +
    ...             "Don't even ask for this").encode())
    >>> header, body = browser.request(url)
    >>> body
    'Keep this for a while'

Sometimes the server will explicitly state that caches are not to be used.
In this case the response contains __no-store__ for the value of the 
  __Cache-Control__ header.

    >>> url = "http://test.test/do_not_cache_me"
    >>> test.socket.respond(url=url, 
    ...   response=("HTTP/1.0 200 Ok\r\n" +
    ...             "Cache-Control: no-store\r\n" +
    ...             "\r\n" +
    ...             "Don't cache me").encode())
    >>> header, body = browser.request(url)
    >>> body
    "Don't cache me"
    >>> test.socket.respond(url=url, 
    ...   response=("HTTP/1.0 200 Ok\r\n" +
    ...             "Cache-Control: no-store\r\n" +
    ...             "\r\n" +
    ...             "Ask for this").encode())
    >>> header, body = browser.request(url)
    >>> body
    'Ask for this'
    
A cache should be able to hold multiple responses, and keep them separate.
Here we cache, then change, another URL and check that both of the URLs cached
  so far are present.

    >>> url = "http://test.test/cache_me2"
    >>> test.socket.respond(url=url, 
    ...   response=("HTTP/1.0 200 Ok\r\n" +
    ...             "Cache-Control: max-age=9001\r\n" + 
    ...             "\r\n" +
    ...             "Keep this for a while, also").encode())
    >>> header, body = browser.request(url)
    >>> body
    'Keep this for a while, also'
    >>> test.socket.respond(url=url, 
    ...   response=("HTTP/1.0 200 Ok\r\n" +
    ...             "Cache-Control: max-age=9001\r\n" +
    ...             "\r\n" +
    ...             "Don't even ask for this").encode())
    >>> header, body = browser.request(url)
    >>> body
    'Keep this for a while, also'
    >>> header, body = browser.request("http://test.test/cache_me1")
    >>> body
    'Keep this for a while'
    
A cached entry can be invalidated by time elapsing, so here we cache a response
  with a one second life and wait for it to be invalidated.

    >>> url = "http://test.test/cache_me3"
    >>> test.socket.respond(url=url, 
    ...   response=("HTTP/1.0 200 Ok\r\n" +
    ...             "Cache-Control: max-age=1\r\n" + 
    ...             "\r\n" +
    ...             "Keep this for a short while").encode())
    >>> header, body = browser.request(url)
    >>> body
    'Keep this for a short while'
    >>> test.socket.respond(url=url, 
    ...   response=("HTTP/1.0 200 Ok\r\n" +
    ...             "\r\n" +
    ...             "Don't ask for this immediately").encode())
    >>> header, body = browser.request(url)
    >>> body
    'Keep this for a short while'
    >>> time.sleep(2)
    >>> header, body = browser.request(url)
    >>> body
    "Don't ask for this immediately"

Each cached response will have different lifetimes.
The responses cached earlier should still be valid.

    >>> header, body = browser.request("http://test.test/cache_me1")
    >>> body
    'Keep this for a while'
    >>> header, body = browser.request("http://test.test/cache_me2")
    >>> body
    'Keep this for a while, also'
