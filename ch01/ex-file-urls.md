Tests for WBE Chapter 1 Exercise `File URLs`
============================================

Add support for the file scheme, which allows the browser to open
local files. For example, `file:///path/goes/here` should refer to the
file on your computer at location `/path/goes/here`. Also make it so
that, if your browser is started without a URL being given, some
specific file on your computer is opened. You can use that file for
quick testing.

For file URL the `host` and `port` should be `None`. If the file
doesn't exist, raise a `FileNotFoundError`; this should happen
automatically when you call `open`.

Tests 
-----

Testing boilerplate:

    >>> from os import path
    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> import browser


	
Test URLs with a `:` in them
 
    >>> browser.URL("file://C:/Users/test/test.html")
    URL(scheme=file, host=None, port=None, path='C:/Users/test/test.html')
	

Test Windows-style paths
 
    >>> browser.URL("file://C:\\Users\\test\\test.html")
    URL(scheme=file, host=None, port=None, path='C:\\Users\\test\\test.html')
    
	
Test relative paths 

    >>> browser.URL("file://local_file.html")
    URL(scheme=file, host=None, port=None, path='local_file.html')
	


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
    
Requesting a nonexistent file should result in a `FileNotFoundError`:

    >>> browser.URL("file:///this/file/does/not/exist").request()
    Traceback (most recent call last):
      ...
    FileNotFoundError: [Errno 2] No such file or directory: '/this/file/does/not/exist'
