# Tests for Web Browser Engineering exercises

The markdown files in this repository contain tests for your web browser.
For example, the file `chapter1-base-tests.md` contains basic unit tests
    for your browser at the end of Chapter 1,
    while `chapter1-exercise-caching-tests.md` contains tests
    for the "Caching" exercise.
You'll be graded on passing both the `base` and `exercise` tests.

Read through the test files for each chapter before working on the web
    browser.
The test files contain additional information about how you should
    implement each exercise and how it will be tested.
Note that this repository will be updated throughout the quarter with
   new tests for each chapter.

## Running the tests

You do not need to run these tests manually.
They will be automatically run by Gitlab CI in your student repository.
The output should look like this:

    $ python3 src/run-tests.py
    
    Summarised results

                      chapter1-base-tests.md: passed
         chapter1-exercise-http-1-1-tests.md: passed
        chapter1-exercise-file-urls-tests.md: passed
        chapter1-exercise-redirects-tests.md: passed
          chapter1-exercise-caching-tests.md: passed
    ----------------------------------------------------
                                   Final: all passed

To run the tests manually,
    go to the root directory of your web browser
    run `python3 src/run-tests.py` with no arguments.
The script will look for the `browser.py` file in that directory
    and run all of the tests on that file.

With no arguments this script will test the coming week's homework,
    but you can also specify an
    argument to select a specific chapter's tests.
For example, run `python3 src/run-tests.py chapter1`
    to run the tests for the first chapter.
You can use the argument `all` to run all available tests.

You can also run just the test file for a specific exercise.
    To do so, use the argument `chapter{n}-{exercise-name}`.
    For example: to run the chapter1 base tests (corresponding file name `chapter1-base-tests.md`),
    use the argument `chapter1-base`. To run the chapter1 file url tests (corresponding file name `chapter1-exercise-file-urls-tests.md`),
    use the argument `chapter1-file-urls`

The output of the script is [doctest](https://docs.python.org/3/library/doctest.html)
    output for each markdown file for the current chapter followed by a
    summary of which files contain failed tests.

## Mocked modules and methods

Our test framework _mocks_ certain methods in the standard library,
    meaning it overwrites them for testing purposes.
For example, `socket.socket` no longer creates a real OS socket;
    instead, it creates a mock socket that does not actually make
    connections over the network.
For the tests to work, it's important only to use mocked methods.
Specifically, here are the mocked methods in various modules:

| Library | Methods |
| ------- | ------- |
| `socket` | The `socket` class and its methods `connect`, `send`, `makefile`, `close` |
| `ssl` | The `wrap_socket` function |

This table will be updated throughout the quarter
    as we test more parts of your browser.
