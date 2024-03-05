Tests for WBE Chapter 1 Exercise `File URLs`
============================================

The __file__ scheme allows a web browser to open files on the local computer 
  directly.
In this case there will be no host or port, just the path to the file.

For file URL the `host` and `port` should be `None`.

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
    
Requesting a nonexistent file should result in error.

    >>> wbemocks.errors(browser.URL("file:///this/file/does/not/exist").request)
    True
