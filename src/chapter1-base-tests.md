Tests for WBE Chapter 1
=======================

Chapter 1 (Downloading Web Pages) covers parsing URLs, HTTP requests
and responses, and a very simplistic print function that writes
to the screen. This file contains tests for those components.

Here's the testing boilerplate.

    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> import browser
    

Testing `show`
--------------

The `show` function is supposed to print some HTML to the screen, but
skip the tags inside.

    >>> browser.show('<body>hello</body>')
    hello
    >>> browser.show('<body><wbr>hello</body>')
    hello
    >>> browser.show('<body>he<wbr>llo</body>')
    hello
    >>> browser.show('<body>hel<div>l</div>o</body>')
    hello

Note that the tags do not have to match:

    >>> browser.show('<body><p>hel</div>lo</body>')
    hello
    >>> browser.show('<body>h<p>el<div>l</p>o</div></body>')
    hello
    
Newlines should not be removed:

    >>> browser.show('<body>hello\nworld</body>')
    hello
    world

Testing `request`
-----------------

The `request` function makes HTTP requests.

To test it, we use the `test.socket` object, which mocks the HTTP server:

    >>> url = 'http://test.test/example1'
    >>> test.socket.respond(url=url,
    ...   response=("HTTP/1.0 200 OK\r\n" +
    ...             "Header1: Value1\r\n" + 
    ...             "\r\n" +
    ...             "Body text").encode())

Then we request the URL and test that the browser generated request is proper:

    >>> response_headers, response_body = browser.request(url)
    >>> command, path, version, headers = test.socket.parse_last_request(url)
    >>> command
    'GET'
    >>> path
    '/example1'
    >>> version in {"HTTP/1.0", "HTTP/1.1"}
    True
    >>> headers["host"]
    'test.test'
    
Also check that the browser parsed the response properly

    >>> response_body
    'Body text'
    >>> response_headers
    {'header1': 'Value1'}

Testing SSL support
-------------------

Since this next URL uses https as the scheme the browser should automatically use
  SSL and switch the default port used to 443.

    >>> url = 'https://test.test/example2'
    >>> test.socket.respond(url=url, 
    ...   response=("HTTP/1.0 200 OK\r\n" +
    ...             "\r\n" +
    ...             "SSL working").encode())
    >>> response_headers, response_body = browser.request(url)
    >>> command, path, version, headers = test.socket.parse_last_request(url)
    >>> command
    'GET'
    >>> path
    '/example2'
    >>> version in {"HTTP/1.0", "HTTP/1.1"}
    True
    >>> headers["host"]
    'test.test'
    >>> response_body
    'SSL working'
    >>> response_headers
    {}

SSL support also means some support for specifying ports in the URL.

    >>> url = 'https://test.test:400/example3'
    >>> test.socket.respond(url=url, 
    ...   response=("HTTP/1.0 200 OK\r\n" +
    ...             "\r\n" +
    ...             "Ports working").encode())
    >>> response_headers, response_body = browser.request(url)
    >>> command, path, version, headers = test.socket.parse_last_request(url)
    >>> command
    'GET'
    >>> path
    '/example3'
    >>> version in {"HTTP/1.0", "HTTP/1.1"}
    True
    >>> headers["host"]
    'test.test'
    >>> response_body
    'Ports working'
    >>> response_headers
    {}


Requesting the wrong port is an error.

    >>> test.errors(browser.request, "http://test.test:401/example3")
    True

