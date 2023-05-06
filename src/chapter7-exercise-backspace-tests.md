Tests for WBE Chapter 7 Exercise `Backspace`
============================================

Description
-----------

Add support for the backspace key when typing in the address bar.
Honestly, do this exercise just for your sanity.


Extra Requirements
------------------
* Name the method in the `Browser` class that handles the backspace event
  `handle_backspace`


Test code
---------

Boilerplate.

    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> import browser

Create a response, load it with the browser, then click on the address bar.

    >>> url = 'http://test.test/chapter7-backspace'
    >>> test.socket.respond_200(url, body="Something")
    >>> this_browser = browser.Browser()
    >>> this_browser.load(url)
    >>> this_browser.handle_click(test.Event(50, 51))
    >>> this_browser.focus
    'address bar'

This should clear out the text in the address bar, so type some things into it.

    >>> len(this_browser.address_bar)
    0
    >>> for c in "Mickey Mouse":
    ...   this_browser.handle_key(test.key_event(c))
    >>> this_browser.address_bar
    'Mickey Mouse'

Pressing the backspace key (delete on Macs) should remove the rightmost
  character.

    >>> this_browser.handle_backspace(test.backspace_event)
    >>> this_browser.address_bar
    'Mickey Mous'

    >>> this_browser.handle_backspace(test.backspace_event)
    >>> this_browser.address_bar
    'Mickey Mou'

    >>> this_browser.handle_backspace(test.backspace_event)
    >>> this_browser.address_bar
    'Mickey Mo'

You should still be able to type letters after backspace-ing.

    >>> this_browser.handle_key(test.key_event('o'))
    >>> this_browser.handle_key(test.key_event('s'))
    >>> this_browser.handle_key(test.key_event('e'))
    >>> this_browser.address_bar
    'Mickey Moose'

Clearing out the entire address bar should be possible.

    >>> while len(this_browser.address_bar) > 0:
    ...   this_browser.handle_backspace(test.backspace_event)
    >>> len(this_browser.address_bar)
    0

Pressing backspace with an empty address bar should cause no change.

    >>> this_browser.handle_backspace(test.backspace_event)
    >>> len(this_browser.address_bar)
    0

    >>> this_browser.handle_backspace(test.backspace_event)
    >>> len(this_browser.address_bar)
    0


Finally, typing letters should still function.

    >>> for c in "Donald Duck":
    ...   this_browser.handle_key(test.key_event(c))
    >>> this_browser.address_bar
    'Donald Duck'
