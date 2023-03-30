Tests for WBE Chapter 1 Exercise `Redirects`
============================================

Testing boilerplate:

    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> import browser

When a response from the server has an HTTP code in the 300s
  it is a redirect.
The browser should use the URL located in the __Location__ header
  of the response to find where the content is now.

    >>> from_url = 'http://test.test/redirect1'
    >>> to_url = 'http://test.redirect_test/target1'
    >>> test.socket.respond(url=from_url, 
    ...   response=("HTTP/1.0 301 Moved Permanently\r\n" +
    ...             "Location: {}\r\n" +
    ...             "\r\n").format(to_url).encode())
    >>> test.socket.respond(url=to_url,
    ...   response=("HTTP/1.0 200 Ok\r\n" +
    ...             "\r\n" +
    ...             "You found me").encode())
    >>> headers, body = browser.request(from_url)
    >>> body
    'You found me'
    
This __Location__ header may contain a full URL, as seen above, or
  omit the scheme and host as seen here.

    >>> from_url = 'http://test.test/redirect2'
    >>> to_url = 'http://test.test/target2'
    >>> test.socket.respond(url=from_url, 
    ...   response=("HTTP/1.0 301 Moved Permanently\r\n" +
    ...             "Location: /target2\r\n" + 
    ...             "\r\n").encode())
    >>> test.socket.respond(url=to_url, 
    ...   response=("HTTP/1.0 200 Ok\r\n"
    ...             "\r\n" +
    ...             "You found me again").encode())
    >>> headers, body = browser.request(from_url)
    >>> body
    'You found me again'
    
The result of a redirect may be another redirect which forms
  a chain to the requested content.
Now that you have seen the content of the redirect response we
  will use a helper function to make the linkage clearer.

    >>> start_url = 'http://test.test/redirect3'
    >>> middle_url = 'http://test.test/target3'
    >>> final_url = 'http://test.redirect_test/target4'
    >>> test.socket.redirect_url(from_url=start_url, to_url=middle_url)
    >>> test.socket.redirect_url(from_url=middle_url, to_url=final_url)
    >>> test.socket.respond(url=final_url,
    ...   response=("HTTP/1.0 200 Ok\r\n" +
    ...             "\r\n" +
    ...             "I need to hide better").encode())
    >>> headers, body = browser.request(start_url)
    >>> body
    'I need to hide better'

Redirection opens up the possibly for infinite loops, these should
  lead to an error.
The simplest infinite loop is a redirect to itself.

    >>> url = 'http://test.test/redirect4'
    >>> test.socket.redirect_url(from_url=url, to_url=url)
    >>> test.errors(browser.request, url)
    True

Infinite loops can be more complex, this is a two stage loop.

    >>> url1 = 'http://test.test/redirect5'
    >>> url2 = 'http://test.test/target5'
    >>> test.socket.redirect_url(from_url=url1, to_url=url2)
    >>> test.socket.redirect_url(from_url=url2, to_url=url1)
    >>> test.errors(browser.request, url1)
    True
    >>> test.errors(browser.request, url2)
    True

The browser should not perform a redirect for non 3XX status codes, even if
  a __Location__ header is present

    >>> url = 'http://test.test/not_redirect'
    >>> do_not_follow = 'http://test.test/not_target'
    >>> test.socket.respond(url=url, 
    ...   response=("HTTP/1.0 200 OK\r\n" +
    ...             "Location: {}\r\n" +
    ...             "\r\n" +
    ...             "Stay here").format(do_not_follow).encode())
    >>> test.socket.respond(url=do_not_follow, 
    ...   response=("HTTP/1.0 200 Ok\r\n" +
    ...             "\r\n" +
    ...             "Too far").encode())
    >>> header, body = browser.request(url)
    >>> body
    'Stay here'


