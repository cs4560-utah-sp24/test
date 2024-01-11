Tests for WBE Chapter 1
=======================

Chapter 1 (Downloading Web Pages) covers parsing URLs, HTTP requests
and responses, and a very simplistic print function that writes
to the screen. This file contains tests for those components.

Here's the testing boilerplate.

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
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

To test it, we use the `wbemocks.socket` object, which mocks the HTTP server:

    >>> url = 'http://wbemocks.test/example1'
    >>> wbemocks.socket.respond(url=url,
    ...   response=("HTTP/1.0 200 OK\r\n" +
    ...             "\r\n" +
    ...             "Body text").encode())

Then we request the URL and test that the browser generated request is proper:

    >>> response_body = browser.URL(url).request()
    >>> command, path, version, headers = wbemocks.socket.parse_last_request(url)
    >>> command
    'GET'
    >>> path
    '/example1'
    >>> version in {"HTTP/1.0", "HTTP/1.1"}
    True
    >>> headers["host"]
    'wbemocks.test'
    
Also check that the browser parsed the response properly

    >>> response_body
    'Body text'

Testing SSL support
-------------------

Since this next URL uses https as the scheme the browser should automatically use
  SSL and switch the default port used to 443.

    >>> url = 'https://wbemocks.test/example2'
    >>> wbemocks.socket.respond(url=url, 
    ...   response=("HTTP/1.0 200 OK\r\n" +
    ...             "\r\n" +
    ...             "SSL working").encode())
    >>> response_body = browser.URL(url).request()
    >>> command, path, version, headers = wbemocks.socket.parse_last_request(url)
    >>> command
    'GET'
    >>> path
    '/example2'
    >>> version in {"HTTP/1.0", "HTTP/1.1"}
    True
    >>> headers["host"]
    'wbemocks.test'
    >>> response_body
    'SSL working'

SSL support also means some support for specifying ports in the URL.

    >>> url = 'https://wbemocks.test:400/example3'
    >>> wbemocks.socket.respond(url=url, 
    ...   response=("HTTP/1.0 200 OK\r\n" +
    ...             "\r\n" +
    ...             "Ports working").encode())
    >>> response_body = browser.URL(url).request()
    >>> command, path, version, headers = wbemocks.socket.parse_last_request(url)
    >>> command
    'GET'
    >>> path
    '/example3'
    >>> version in {"HTTP/1.0", "HTTP/1.1"}
    True
    >>> headers["host"]
    'wbemocks.test'
    >>> response_body
    'Ports working'


Requesting the wrong port is an error.

    >>> browser.URL("http://wbemocks.test:401/example3").request()
    Traceback (most recent call last):
       ...
    AssertionError: You are requesting a url that you shouldn't: http://wbemocks.test:401/example3

