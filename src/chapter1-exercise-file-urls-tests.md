Tests for WBE Chapter 1 Exercise `File URLs`
============================================

Testing boilerplate:

    >>> from os import path
    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> import browser

The __file__ scheme allows a web browser to open files on the local computer 
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
    >>> headers, body = browser.request(url)
    >>> body
    'Hello world'
    
Requesting a nonexistent file should result in error.

    >>> test.errors(browser.request, "file:///this/file/does/not/exist")
    True
