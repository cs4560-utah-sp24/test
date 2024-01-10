Tests for WBE Chapter 2 Exercise `Mouse Wheel`
==============================================

Testing boilerplate:

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> _ = wbemocks.patch_canvas()
    >>> import browser

Note: This test was removed because it was difficult to get it to pass on all 3 major OSes.

To course staff: see git history for a copy of the old wbemocks.
