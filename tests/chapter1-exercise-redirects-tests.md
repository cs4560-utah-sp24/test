Tests for WBE Chapter 1 Exercise `Redirects`
============================================

Testing boilerplate:

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> import browser

When a response from the server has an HTTP code in the 300s
  it is a redirect.
The browser should use the URL located in the __Location__ header
  of the response to find where the content is now.

    >>> from_url = 'http://wbemocks.test/redirect1'
    >>> to_url = 'http://wbemocks.redirect_test/target1'
    >>> wbemocks.socket.respond(url=from_url, 
    ...   response=("HTTP/1.0 301 Moved Permanently\r\n" +
    ...             "Location: {}\r\n" +
    ...             "\r\n").format(to_url).encode())
    >>> wbemocks.socket.respond(url=to_url,
    ...   response=("HTTP/1.0 200 Ok\r\n" +
    ...             "\r\n" +
    ...             "You found me").encode())
    >>> body = browser.URL(from_url).request()
    >>> body
    'You found me'
    
This __Location__ header may contain a full URL, as seen above, or
  omit the scheme and host as seen here.

    >>> from_url = 'http://wbemocks.test/redirect2'
    >>> to_url = 'http://wbemocks.test/target2'
    >>> wbemocks.socket.respond(url=from_url, 
    ...   response=("HTTP/1.0 301 Moved Permanently\r\n" +
    ...             "Location: /target2\r\n" + 
    ...             "\r\n").encode())
    >>> wbemocks.socket.respond(url=to_url, 
    ...   response=("HTTP/1.0 200 Ok\r\n"
    ...             "\r\n" +
    ...             "You found me again").encode())
    >>> body = browser.URL(from_url).request()
    >>> body
    'You found me again'
    
The result of a redirect may be another redirect which forms
  a chain to the requested content.
Now that you have seen the content of the redirect response we
  will use a helper function to make the linkage clearer.

    >>> start_url = 'http://wbemocks.test/redirect3'
    >>> middle_url = 'http://wbemocks.test/target3'
    >>> final_url = 'http://wbemocks.redirect_test/target4'
    >>> wbemocks.socket.redirect_url(from_url=start_url, to_url=middle_url)
    >>> wbemocks.socket.redirect_url(from_url=middle_url, to_url=final_url)
    >>> wbemocks.socket.respond(url=final_url,
    ...   response=("HTTP/1.0 200 Ok\r\n" +
    ...             "\r\n" +
    ...             "I need to hide better").encode())
    >>> body = browser.URL(start_url).request()
    >>> body
    'I need to hide better'

Redirection opens up the possibly for infinite loops, these should
  lead to an error.
The simplest infinite loop is a redirect to itself.

    >>> url = 'http://wbemocks.test/redirect4'
    >>> wbemocks.socket.redirect_url(from_url=url, to_url=url)
    >>> wbemocks.errors(browser.URL(url).request)
    True

Infinite loops can be more complex, this is a two stage loop.

    >>> url1 = 'http://wbemocks.test/redirect5'
    >>> url2 = 'http://wbemocks.test/target5'
    >>> wbemocks.socket.redirect_url(from_url=url1, to_url=url2)
    >>> wbemocks.socket.redirect_url(from_url=url2, to_url=url1)
    >>> wbemocks.errors(browser.URL(url1).request)
    True
    >>> wbemocks.errors(browser.URL(url2).request)
    True

The browser should not perform a redirect for non 3XX status codes, even if
  a __Location__ header is present

    >>> url = 'http://wbemocks.test/not_redirect'
    >>> do_not_follow = 'http://wbemocks.test/not_target'
    >>> wbemocks.socket.respond(url=url, 
    ...   response=("HTTP/1.0 200 OK\r\n" +
    ...             "Location: {}\r\n" +
    ...             "\r\n" +
    ...             "Stay here").format(do_not_follow).encode())
    >>> wbemocks.socket.respond(url=do_not_follow, 
    ...   response=("HTTP/1.0 200 Ok\r\n" +
    ...             "\r\n" +
    ...             "Too far").encode())
    >>> body = browser.URL(url).request()
    >>> body
    'Stay here'


