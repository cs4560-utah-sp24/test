Tests for WBE Chapter 1 Exercise `HTTP/1.1`
===========================================

Testing boilerplate:

    >>> import time
    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> import browser

Mock the HTTP server, as before:

    >>> url = 'http://test.test/example1'
    >>> test.socket.respond(url=url,
    ...   response=("HTTP/1.0 200 OK\r\n" +
    ...             "Header1: Value1\r\n" + 
    ...             "\r\n" +
    ...             "Body text").encode(),
    ...   method="GET")

This request/response pair was tested in the base tests, but now we are 
  checking that the __Connection__ header is present and contains __close__, that a
  __User-Agent__ header is present, and that the request is HTTP 1.1:

    >>> response_headers, response_body = browser.request(url)
    >>> command, path, version, headers = test.socket.parse_last_request(url)
    >>> command
    'GET'
    >>> path
    '/example1'
    >>> headers["connection"]
    'close'
    >>> "user-agent" in headers
    True
    >>> version
    'HTTP/1.1'

Use a new mock HTTP server with a new URL to avoid possible caching errors.

    >>> url = 'http://test.test/example2'
    >>> test.socket.respond(url=url,
    ...   response=("HTTP/1.0 200 OK\r\n" +
    ...             "Header2: Value2\r\n" + 
    ...             "\r\n" +
    ...             "Body text").encode(),
    ...   method="GET")


In addition to these changes, the signature of your `request` function should 
  now include an optional argument, `headers`, which is a dictionary mapping 
  strings to strings representing header names mapping to their values.

**Warning**: Default values for optional arguments in Python generally should
not be mutable objects like dictionaries, for reasons detailed in the
[Python guide](https://docs.python-guide.org/writing/gotchas/#default-args).
    
    >>> extra_client_headers = {"ClientHeader" : "42"}
    >>> headers, body = browser.request(url, headers=extra_client_headers)
    >>> command, path, version, headers = test.socket.parse_last_request(url)
    >>> headers["clientheader"]
    '42'

Use a new mock HTTP server with a new URL to avoid possible caching errors.

    >>> url = 'http://test.test/example3'
    >>> test.socket.respond(url=url,
    ...   response=("HTTP/1.0 200 OK\r\n" +
    ...             "Header2: Value2\r\n" + 
    ...             "\r\n" +
    ...             "Body text").encode(),
    ...   method="GET")

If the `headers` argument includes headers that are sent by default, like `User-Agent`,
    the `headers` argument should overwrite their value.
In other words, the request should only contain one occurrence of each header.
  
    >>> extra_client_headers = {"User-Agent" : "different/1.0"}
    >>> headers, body = browser.request(url, headers=extra_client_headers)
    >>> test.socket.count_header_last_request(url, "User-Agent")
    1
    >>> command, path, version, headers = test.socket.parse_last_request(url)
    >>> headers["user-agent"]
    'different/1.0'

Remember that headers are case-insensitive:

    >>> extra_client_headers = {"user-agent" : "a/1.0", "User-Agent" : "b/1.0"}
    >>> headers, body = browser.request(url, headers=extra_client_headers)
    >>> test.socket.count_header_last_request(url, "User-Agent")
    1
