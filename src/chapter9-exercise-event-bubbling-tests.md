Tests for WBE Chapter 9 Exercise `Event Bubbling`
============================================

Description
-----------

Right now, you can attach a click handler to a elements, but not to anything
    else.
Fix this.
One challenge you’ll face is that when you click on an element, you also click
    on all its ancestors.
On the web, this sort of quirk is handled by event bubbling: when an event is
    generated on an element, listeners are run not just on that element but
    also on its ancestors.
Implement event bubbling, and make sure listeners can call stopPropagation on
    the event object to stop bubbling the event up the tree.
Double-check that clicking on links still works, and make sure preventDefault
    still successfully prevents clicks on a link from actually following the
    link.


Test code
---------

Boilerplate.

    >>> import test
    >>> _ = test.socket.patch().start()
    >>> _ = test.ssl.patch().start()
    >>> test.NORMALIZE_FONT = True
    >>> import browser

Set up the webpage and script links.

    >>> web_url = 'http://test.test/chapter9-bubble-1/html'
    >>> script_url = 'http://test.test/chapter9-bubble-1/js'
    >>> html = ("<script src=" + script_url + "></script>"
    ...       + "<div><form><input name=bubbles value=sugar></form></div>")
    >>> test.socket.respond_200(web_url, body=html)

Attach an event listener to each nested element.
Click an show that all event listeners are called in the correct order.

    >>> script = """
    ... document.querySelectorAll('div')[0].addEventListener('click',
    ...   function(e) {
    ...     console.log('div saw a click');
    ...   });
    ... document.querySelectorAll('form')[0].addEventListener('click',
    ...   function(e) {
    ...     console.log('form saw a click');
    ...   });
    ... document.querySelectorAll('input')[0].addEventListener('click',
    ...   function(e) {
    ...     console.log('input saw a click');
    ...   });
    ... """
    >>> test.socket.respond_200(script_url, body=script)
    >>> this_browser = browser.Browser()
    >>> this_browser.load(web_url)
    >>> this_browser.handle_click(test.Event(20, 100 + 24))
    input saw a click
    form saw a click
    div saw a click
    >>> this_browser.tabs[0].js.run("document.querySelectorAll('input')[0].getAttribute('value')")
    ''

Setup a new webpage with the same content but a different script.
This time prevent the default in the input.

    >>> web_url = 'http://test.test/chapter9-bubble-2/html'
    >>> script_url = 'http://test.test/chapter9-bubble-2/js'
    >>> html = ("<script src=" + script_url + "></script>"
    ...       + "<div><form><input name=bubbles value=sugar></form></div>")
    >>> test.socket.respond_200(web_url, body=html)
    >>> script = """
    ... document.querySelectorAll('div')[0].addEventListener('click',
    ...   function(e) {
    ...     console.log('div saw a click');
    ...   });
    ... document.querySelectorAll('form')[0].addEventListener('click',
    ...   function(e) {
    ...     console.log('form saw a click');
    ...   });
    ... document.querySelectorAll('input')[0].addEventListener('click',
    ...   function(e) {
    ...     console.log('input saw a click');
    ...     e.preventDefault();
    ...   });
    ... """
    >>> test.socket.respond_200(script_url, body=script)
    >>> this_browser = browser.Browser()
    >>> this_browser.load(web_url)
    >>> this_browser.handle_click(test.Event(20, 100 + 24))
    input saw a click
    form saw a click
    div saw a click
    >>> this_browser.tabs[0].js.run("document.querySelectorAll('input')[0].getAttribute('value')")
    'sugar'

Stopping propagation should also work.

    >>> web_url = 'http://test.test/chapter9-bubble-3/html'
    >>> script_url = 'http://test.test/chapter9-bubble-3/js'
    >>> html = ("<script src=" + script_url + "></script>"
    ...       + "<div><form><input name=bubbles value=sugar></form></div>")
    >>> test.socket.respond_200(web_url, body=html)
    >>> script = """
    ... document.querySelectorAll('div')[0].addEventListener('click',
    ...   function(e) {
    ...     console.log('div saw a click');
    ...   });
    ... document.querySelectorAll('form')[0].addEventListener('click',
    ...   function(e) {
    ...     console.log('form saw a click');
    ...     e.stopPropagation();
    ...   });
    ... document.querySelectorAll('input')[0].addEventListener('click',
    ...   function(e) {
    ...     console.log('input saw a click');
    ...   });
    ... """
    >>> test.socket.respond_200(script_url, body=script)
    >>> this_browser = browser.Browser()
    >>> this_browser.load(web_url)
    >>> this_browser.handle_click(test.Event(20, 100 + 24))
    input saw a click
    form saw a click
    >>> this_browser.tabs[0].js.run("document.querySelectorAll('input')[0].getAttribute('value')")
    ''

Both should be able to work on the same click.

    >>> web_url = 'http://test.test/chapter9-bubble-4/html'
    >>> script_url = 'http://test.test/chapter9-bubble-4/js'
    >>> html = ("<script src=" + script_url + "></script>"
    ...       + "<div><form><input name=bubbles value=sugar></form></div>")
    >>> test.socket.respond_200(web_url, body=html)
    >>> script = """
    ... document.querySelectorAll('div')[0].addEventListener('click',
    ...   function(e) {
    ...     console.log('div saw a click');
    ...   });
    ... document.querySelectorAll('form')[0].addEventListener('click',
    ...   function(e) {
    ...     console.log('form saw a click');
    ...   });
    ... document.querySelectorAll('input')[0].addEventListener('click',
    ...   function(e) {
    ...     console.log('input saw a click');
    ...     e.preventDefault();
    ...     e.stopPropagation();
    ...   });
    ... """
    >>> test.socket.respond_200(script_url, body=script)
    >>> this_browser = browser.Browser()
    >>> this_browser.load(web_url)
    >>> this_browser.handle_click(test.Event(20, 100 + 24))
    input saw a click
    >>> this_browser.tabs[0].js.run("document.querySelectorAll('input')[0].getAttribute('value')")
    'sugar'
