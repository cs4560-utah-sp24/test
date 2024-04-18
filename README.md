CS 4560 Web Browser Internals
=============================

This repository contains the autograder tests for CS 4560 plus various
class-relevant files.

Using this repository
---------------------

In the Github repository we create for you, run:

	git submodule update --init

This command downloads this repository in the `test` subdirectory. If
this command errors out and the error message contains the text
`git@github.com: Permission denied (publickey)` you can fix it by
either [adding an SSH key][ssh-key] to your Github account or by
running

[ssh-key]: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account

	git clone https://github.com/cs4560-utah-sp24/test.git

from inside your repository.

Throughout the class, we'll likely push new versions of this
repository, to fix bugs or maybe update class-relevant files. You can
update the copy on your computer by running:

	git submodule update --remote
	
When you do this, `git diff` or `git commit` or whatever other
commands will show changes to the `.gitmodules` file; those are fine,
go ahead and commit/push them together with any other changes.

By running the `run.py` script. Specifically, from your main
repository run:

    $ python3 test/run.py
    
    Summarised results

                                ch01/base.md: passed
                          ch01/ex-http-11.md: passed
                        ch01/ex-file-urls.md: passed
                        ch01/ex-redirects.md: passed
                          ch01/ex-caching.md: passed
    ----------------------------------------------------
                                   Final: all passed

The same exact script is run by the autograder in Github Actions.

The tests
---------

You can find the tests themselves folders `ch01` through `ch10`. The
`base.md` file always contains tests for the base browser from the
book. You should get those passing first. The `ex-X.md` file contains
the tests for the named exercise. Before doing those, look at the
file. It may indicate additional functions you have to implement for
testing (beyond those of the book itself) or have hints, additional
rules, or further explanations. You'll be graded on passing both the
"base" and "exercise" tests.

The full list of exercises planned to assign in CS 4560 are:

**Chapter 1**: HTTP/1.1, `file://` URLs, redirects, caching

**Chapter 2**: Line breaks, resizing, scrollbar, emoji

**Chapter 3**: Centered text, superscripts, soft hyphens, small caps

**Chapter 4**: Comments, paragraphs, scripts, quoted attributes

**Chapter 5**: Links bar, hidden head, bullets, anonymous block boxes

**Chapter 6**: Fonts, width/height, class selectors, shorthand properties

**Chapter 7**: Backspace, middle-click, fragments, bookmarks

**Chapter 8**: Enter key, GET forms, check boxes, rich buttons

**Chapter 9**: `Node.children`, `createElement`, IDs, event bubbling

**Chapter 10**: New inputs, certificate errors, script access, referer

Note that the exercises assigned for future chapters may change
without notice during the semester.

Running the tests
-----------------

When run, the `run.py` script runs all tests for the current chapter.
But there are some additional options that might be handy:

The first argument select a specific chapter. For example, `python3
run.py ch1` runs the tests for the first chapter. You can use the
argument `all` to run all available tests.

The first argument can also select a specific exercise. For example,
`python3 run.py ch1-base` runs the base tests for the first chapter,
while `python3 run.py ch1-file-urls` runs tests for the file URLs
exercise.

The tests themselves are written in Markdown using [doctest][doctest]
to run them. Any failing tests will output the relevant paragraph of
Markdown explanation as well as the expected and actual output. To
help with `print`-debugging, any line of output beginning with `!dbg`
is ignored.

[doctest]: https://docs.python.org/3/library/doctest.html

The test framework _mocks_ certain methods in the standard library,
meaning it overwrites them for testing purposes. For example,
`socket.socket` no longer creates a real OS socket; instead, it
creates a mock socket that does not actually make connections over the
network. This makes the tests reproducible and also makes it possible
for the test framework to, for example, inspect the exact bytes sent
over the "socket". For the tests to work, it's important only to use
mocked methods. Specifically, here are the mocked methods in various
modules:

| Library             | Methods                                                           |
|---------------------|-------------------------------------------------------------------|
| `socket`            | `socket`                                                          |
| `socket.socket`     | `connect`, `send`, `makefile`, `close`                            |
| `ssl`               | `wrap_socket`                                                     |
| `certifi`           | `where`, `load_default_certs`, `load_verify_locations`            |
| `tkinter`           | `Tk`, `Canvas`, `font`                                            |
| `tkinter.Tk`        | `bind`                                                            |
| `tkinter.Canvas`    | `create_{text, rectangle, line, oval, polygon}`, `pack`, `delete` |
| `tkinter.font`      | `Font`                                                            |
| `tkinter.font.Font` | `measure`, `metrics`                                              |

File uploads
------------

Whenever you run `run.py`, it uploads a copy of all files imported
from and in the same directory as `browser.py` to the instructor's
server. Your name is also recorded in the upload. This data will be
used to understand mistakes made by students and challenges in
understanding the material. This data will never be made public and
will not affect your grade.

If you don't want to participate, just pass `--no-upload` to `run.py`.
As before, this will not affect your grade.
