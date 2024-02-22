Tests for WBE Chapter 7 Exercise `Backspace`
============================================

Add support for the backspace key when typing in the address bar.
Honestly, do this exercise just for your sanity.

Name the method in the `Browser` class that handles the backspace
event `handle_backspace`. Don't forget to bind `<Backspace>` to it.

Test code
---------

Boilerplate.

    >>> import wbemocks
    >>> _ = wbemocks.socket.patch().start()
    >>> _ = wbemocks.ssl.patch().start()
    >>> import browser

Create a response, load it with the browser, then click on the address bar.

    >>> url = browser.URL(wbemocks.socket.serve("Something"))
    >>> this_browser = browser.Browser()
    >>> this_browser.new_tab(url)
    >>> this_browser.handle_click(wbemocks.ClickEvent(50, 51))
    >>> this_browser.chrome.focus
    'address bar'

This should clear out the text in the address bar, so type some things into it.

    >>> len(this_browser.chrome.address_bar)
    0
    >>> for c in "Mickey Mouse":
    ...   this_browser.handle_key(wbemocks.KeyEvent(c))
    >>> this_browser.chrome.address_bar
    'Mickey Mouse'

Pressing the backspace key (delete on Macs) should remove the rightmost
character.

    >>> this_browser.handle_backspace(wbemocks.Event())
    >>> this_browser.chrome.address_bar
    'Mickey Mous'

    >>> this_browser.handle_backspace(wbemocks.Event())
    >>> this_browser.chrome.address_bar
    'Mickey Mou'

    >>> this_browser.handle_backspace(wbemocks.Event())
    >>> this_browser.chrome.address_bar
    'Mickey Mo'

You should still be able to type letters after backspace-ing.

    >>> this_browser.handle_key(wbemocks.KeyEvent('o'))
    >>> this_browser.handle_key(wbemocks.KeyEvent('s'))
    >>> this_browser.handle_key(wbemocks.KeyEvent('e'))
    >>> this_browser.chrome.address_bar
    'Mickey Moose'

Clearing out the entire address bar should be possible.

    >>> for i in range(12):
    ...   this_browser.handle_backspace(wbemocks.Event())
    >>> len(this_browser.chrome.address_bar)
    0

Pressing backspace with an empty address bar should cause no change.

    >>> this_browser.handle_backspace(wbemocks.Event())
    >>> len(this_browser.chrome.address_bar)
    0

    >>> this_browser.handle_backspace(wbemocks.Event())
    >>> len(this_browser.chrome.address_bar)
    0


Finally, typing letters should still function.

    >>> for c in "Donald Duck":
    ...   this_browser.handle_key(wbemocks.KeyEvent(c))
    >>> this_browser.chrome.address_bar
    'Donald Duck'
