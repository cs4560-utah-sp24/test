Tests for WBE Chapter 1 Exercise `File URLs`
============================================

Make sure to add the following method to your URL class:

```
class URL:
    def __repr__(self):
        return "URL(scheme={}, host={}, port={}, path={!r})".format(
            self.scheme, self.host, self.port, self.path)
```

Tests
-----

Testing boilerplate:

    >>> from os import path
    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> import browser

We'll create URLs directly to test that they are parsed correctly:

    >>> browser.URL("file://local_file.txt")
    URL(scheme=file, host=None, port=None, path='local_file.txt')
    >>> browser.URL("file://C:\\Users\\test\\test.html")
    URL(scheme=file, host=None, port=None, path='C:\\Users\\test\\test.html')

The `file` scheme allows a web browser to open files on the local computer 
  directly.
In this case there will be no host or port, just the path to the file.
This also means that there will be no response headers, just a response body.
Here we make a file, put some text in it, and make a file scheme request.

    >>> filename = "local_file.txt"
    >>> full_path = path.abspath(filename)
    >>> with open(full_path, "w") as f:
    ...   f.write("Hello world")
    11
    >>> url = "file://{}".format(full_path)
    >>> body = browser.URL(url).request()
    >>> body
    'Hello world'
    
Requesting a nonexistent file should result in error.

    >>> wbemocks.errors(browser.URL("file:///this/file/does/not/exist").request)
    True
