Tests for WBE Chapter 1 Exercise `Caching`
==========================================

Typically, the same images, styles, and scripts are used on multiple
pages; downloading them repeatedly is a waste. It’s generally valid to
cache any HTTP response, as long as it was requested with GET and
received a 200 response. Implement a cache in your browser and test it
by requesting the same file multiple times. Servers control caches
using the `Cache-Control` header. Add support for this header,
specifically for `no-store` and `max-age` values. If the
`Cache-Control` header contains any other value than these two, it’s
best not to cache the response.

Also don't cache things if the `Cache-Control` header is missing.

Tests
-----

Testing boilerplate:

    >>> import time
    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> import browser

A server response can indicate if the response itself can be cached and for how 
  long.
The __Cache-Control__ header can be set to __max-age=[number]__ to allow caching of
  the response for __[number]__ seconds.
We can test if a browser is caching responses by changing the response and 
  telling the browser to re-request the page.

    >>> url = "http://wbemocks.test/cache_me1"
    >>> wbemocks.socket.respond(url=url, 
    ...   response=("HTTP/1.0 200 Ok\r\n" +
    ...             "Cache-Control: max-age=9001\r\n" +
    ...             "\r\n" +
    ...             "Keep this for a while").encode())
    >>> body = browser.URL(url).request()
    >>> body
    'Keep this for a while'
    >>> wbemocks.socket.respond(url=url, 
    ...   response=("HTTP/1.0 200 Ok\r\n" +
    ...             "Cache-Control: max-age=9001\r\n" +
    ...             "\r\n" +
    ...             "Don't even ask for this").encode())
    >>> body = browser.URL(url).request()
    >>> body
    'Keep this for a while'

Sometimes the server will explicitly state that caches are not to be used.
In this case the response contains __no-store__ for the value of the 
  __Cache-Control__ header.

    >>> url = "http://wbemocks.test/do_not_cache_me"
    >>> wbemocks.socket.respond(url=url, 
    ...   response=("HTTP/1.0 200 Ok\r\n" +
    ...             "Cache-Control: no-store\r\n" +
    ...             "\r\n" +
    ...             "Don't cache me").encode())
    >>> body = browser.URL(url).request()
    >>> body
    "Don't cache me"
    >>> wbemocks.socket.respond(url=url, 
    ...   response=("HTTP/1.0 200 Ok\r\n" +
    ...             "Cache-Control: no-store\r\n" +
    ...             "\r\n" +
    ...             "Ask for this").encode())
    >>> body = browser.URL(url).request()
    >>> body
    'Ask for this'
    
A cache should be able to hold multiple responses, and keep them separate.
Here we cache, then change, another URL and check that both of the URLs cached
  so far are present.

    >>> url = "http://wbemocks.test/cache_me2"
    >>> wbemocks.socket.respond(url=url, 
    ...   response=("HTTP/1.0 200 Ok\r\n" +
    ...             "Cache-Control: max-age=9001\r\n" + 
    ...             "\r\n" +
    ...             "Keep this for a while, also").encode())
    >>> body = browser.URL(url).request()
    >>> body
    'Keep this for a while, also'
    >>> wbemocks.socket.respond(url=url, 
    ...   response=("HTTP/1.0 200 Ok\r\n" +
    ...             "Cache-Control: max-age=9001\r\n" +
    ...             "\r\n" +
    ...             "Don't even ask for this").encode())
    >>> body = browser.URL(url).request()
    >>> body
    'Keep this for a while, also'
    >>> body = browser.URL("http://wbemocks.test/cache_me1").request()
    >>> body
    'Keep this for a while'
    
A cached entry can be invalidated by time elapsing, so here we cache a response
  with a one second life and wait for it to be invalidated.

    >>> url = "http://wbemocks.test/cache_me3"
    >>> wbemocks.socket.respond(url=url, 
    ...   response=("HTTP/1.0 200 Ok\r\n" +
    ...             "Cache-Control: max-age=1\r\n" + 
    ...             "\r\n" +
    ...             "Keep this for a short while").encode())
    >>> body = browser.URL(url).request()
    >>> body
    'Keep this for a short while'
    >>> wbemocks.socket.respond(url=url, 
    ...   response=("HTTP/1.0 200 Ok\r\n" +
    ...             "\r\n" +
    ...             "Don't ask for this immediately").encode())
    >>> body = browser.URL(url).request()
    >>> body
    'Keep this for a short while'
    >>> time.sleep(2)
    >>> body = browser.URL(url).request()
    >>> body
    "Don't ask for this immediately"

Each cached response will have different lifetimes.
The responses cached earlier should still be valid.

    >>> body = browser.URL("http://wbemocks.test/cache_me1").request()
    >>> body
    'Keep this for a while'
    >>> body = browser.URL("http://wbemocks.test/cache_me2").request()
    >>> body
    'Keep this for a while, also'
    
    
 Objective: Verify that your caching mechanism doesn't serve stale data when the scheme, host, or port of the requested URL changes.
 
    >>> URL_base = "http://wbemocks.test/cache_me1"
    >>> wbemocks.socket.respond(url=URL_base,
    ...   response=("HTTP/1.0 200 Ok\r\n" +
    ...             "Cache-Control: max-age=9001\r\n" +
    ...             "\r\n" +
    ...             "Different port page").encode())
    >>> browser.URL(URL_base).request()
    'Different port page'

    >>> URL_diff_scheme = "https://wbemocks.test/cache_me1"
    >>> wbemocks.socket.respond(url=URL_diff_scheme, 
    ...   response=("HTTP/1.0 200 Ok\r\n" +
    ...             "Cache-Control: max-age=9001\r\n" +
    ...             "\r\n" +
    ...             "Different scheme page").encode())
    >>> browser.URL(URL_diff_scheme).request()
    'Different scheme page'

    >>> URL_diff_host = "http://mock.test/cache_me1"
    >>> wbemocks.socket.respond(url=URL_diff_host, 
    ...   response=("HTTP/1.0 200 Ok\r\n" +
    ...             "Cache-Control: max-age=9001\r\n" +
    ...             "\r\n" +
    ...             "Different host page").encode())
    >>> browser.URL(URL_diff_host).request()
    'Different host page'
    
    
    >>> URL_diff_port = "http://wbemocks.test:8080/cache_me1"
    >>> wbemocks.socket.respond(url=URL_diff_port, 
    ...   response=("HTTP/1.0 200 Ok\r\n" +
    ...             "Cache-Control: max-age=9001\r\n" +
    ...             "\r\n" +
    ...             "Keep this PORT for a while").encode())
    >>> browser.URL(URL_diff_port).request()
    'Keep this PORT for a while'
