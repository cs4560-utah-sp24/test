Tests for WBE Chapter 1
=======================

Test support for HTTP/1.1 `Transfer-Encoding: chunked`

Here's the testing boilerplate.

    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> import browser
    

Testing `Transfer-Encoding: chunked` support
-----------------

To test it, we simulate a `chunked` response with `body_text_chunks`

    >>> url = 'http://test.test/example1'
    >>> body_text = ""
    >>> body_text_chunks = ["this\n", "body is\n", "chunked!😈\n"]
    >>> for chunk in body_text_chunks:
    ...   body_text += hex(len(chunk.encode())).split('x')[-1] + "\r\n" + chunk + "\r\n"
    >>> body_text += hex(0).split('x')[-1] + "\r\n" + "" + "\r\n"
    >>> test.socket.respond(url=url,
    ...   response=("HTTP/1.1 200 OK\r\n" +
    ...             "Header1: Value1\r\n" + 
    ...             "Transfer-Encoding: chunked\r\n" +
    ...             "\r\n" +
    ...             body_text).encode())

And check that the browser parsed the response properly:

    >>> response_headers, response_body = browser.request(url)
    >>> command, path, version, headers = test.socket.parse_last_request(url)
    >>> version in {"HTTP/1.1"}
    True
    
    >>> response_body
    'this\nbody is\nchunked!😈\n'