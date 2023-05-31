#!/usr/bin/env python3


import argparse
import doctest
import os
import sys
import re
import datetime

sys.path.append(os.getcwd())


def getCurrentChapter():
    start_time = datetime.date(2023, 3, 27)
    current_time = datetime.date.today()
    for i in range(11):
        if current_time >= start_time:
            start_time += datetime.timedelta(days = 7)
        else:
            return i

    print("Error: current date not in the quarter!")
    return 1


DEFAULT_CICD = f"chapter{getCurrentChapter()}"

CURRENT_TESTS = {
    "chapter1": ["chapter1-base-tests.md",
                 "chapter1-exercise-http-1-1-tests.md",
                 "chapter1-exercise-file-urls-tests.md",
                 "chapter1-exercise-redirects-tests.md",
                 "chapter1-exercise-caching-tests.md",
                 # "chapter1-binary-tests.md",
                 ],
    "chapter2": ["chapter2-base-tests.md",
                 "chapter2-exercise-line-breaks-tests.md",
                 "chapter2-exercise-resizing-tests.md",
                 "chapter2-exercise-mouse-wheel-tests.md",
                 "chapter2-exercise-zoom-tests.md",
                 ],
    "chapter3": ["chapter3-base-tests.md",
                 "chapter3-exercise-centered-text-tests.md",
                 "chapter3-exercise-superscripts-tests.md",
                 "chapter3-exercise-soft-hyphens-tests.md",
                 "chapter3-exercise-small-caps-tests.md",
                 ],
    "chapter4": ["chapter4-base-tests.md",
                 "chapter4-exercise-comments-tests.md",
                 "chapter4-exercise-paragraphs-tests.md",
                 "chapter4-exercise-scripts-tests.md",
                 "chapter4-exercise-quoted-attributes-tests.md",
                 ],
    "chapter5": ["chapter5-base-tests.md",
                 "chapter5-exercise-hidden-head-tests.md",
                 "chapter5-exercise-bullets-tests.md",
                 "chapter5-exercise-scrollbar-tests.md",
                 "chapter5-exercise-links-bar-tests.md",
                 ],
    "chapter6": ["chapter6-base-tests.md",
                 "chapter6-exercise-fonts-tests.md",
                 "chapter6-exercise-width-height-tests.md",
                 "chapter6-exercise-class-selectors-tests.md",
                 "chapter6-exercise-shorthand-properties-tests.md",
                 ],
    "chapter7": ["chapter7-base-tests.md",
                 "chapter7-exercise-backspace-tests.md",
                 "chapter7-exercise-middle-click-tests.md",
                 "chapter7-exercise-fragments-tests.md",
                 "chapter7-exercise-bookmarks-tests.md",
                 ],
    "chapter8": ["chapter8-base-tests.md",
                 "chapter8-exercise-enter-key-tests.md",
                 "chapter8-exercise-check-boxes-tests.md",
                 "chapter8-exercise-tab-tests.md",
                 "chapter8-exercise-get-forms-tests.md",
                 ],
    "chapter9": ["chapter9-base-tests.md",
                 "chapter9-exercise-create-element-tests.md",
                 "chapter9-exercise-node-children-tests.md",
                 "chapter9-exercise-ids-tests.md",
                 "chapter9-exercise-event-bubbling-tests.md",
                 ],
    "chapter10": ["chapter10-base-tests.md",
                  "chapter10-exercise-new-inputs-tests.md",
                  "chapter10-exercise-certificate-errors-tests.md",
                  "chapter10-exercise-script-access-tests.md",
                  "chapter10-exercise-referer-tests.md",
                  ],
}

all_tests = list()
specific_file_tests = {}

'''
add option to run all tests by running script w/ argval 'all',
and add option to run individual test files by name (removing '-exercise-' infix substring if present)
'''
for chapterkey, tests in CURRENT_TESTS.items():
    all_tests.extend(tests)

    specific_file_tests[chapterkey + '-exercises'] = tests[1:]

    for i, test in enumerate(tests):
        arg_val = re.sub(r'-exercise', '', test)
        arg_val = re.sub(r'-tests.md', '', arg_val)
        specific_file_tests[arg_val] = [test]
        specific_file_tests[chapterkey + '-' + str(i + 1)] = [test]

CURRENT_TESTS["all"] = all_tests

CURRENT_TESTS.update(specific_file_tests)

# Below this are a variety of "fixes" to doctest that make it more user-friendly

old_truncate = doctest._SpoofOut.truncate

def patched_truncate(self, size=None):
    """
    Patch the fake doctest stdout to save the output long enough to use when reporting errors
    """
    self._old_getvalue = self.getvalue()
    old_truncate(self, size)

def patched_report_unexpected_exception(self, out, test, example, exc_info):
    """
    Patch the doctest printer to print output when exceptions occur.

    Note that this uses the _old_getvalue saved above, which doctest otherwise throws out
    when exceptions are thrown.
    """
    got = self._fakeout._old_getvalue
    out(self._failure_header(test, example) +
        self._checker.output_difference(example, got, self.optionflags) +
        'Exception Raised:\n' + doctest._indent(doctest._exception_traceback(exc_info)))

old_parse = doctest.DocTestParser.parse

def patched_parse(self, string, name="<string>"):
    """
    Save the text introducing each example to the parser object, so
    that we can use it in the _failure_header.
    """
    output = old_parse(self, string, name)
    self._parsed = output
    return output

old_get_doctest = doctest.DocTestParser.get_doctest

def patched_get_doctest(self, string, globs, name, filename, lineno):
    """
    Copy the text introducing each example from the parser object to
    the doctest object, so that we can use it in the _failure_header.
    """
    out = old_get_doctest(self, string, globs, name, filename, lineno)
    out._parsed = self._parsed
    return out

def patched_failure_header(self, test, example):
    """
    Print the full block being executed, including the text
    introducing the block and going up to the failing example, any
    time a failure occurs.

    To do so, we make use of the _parsed field on the doctest object,
    which saves the complete parsed doctest file. In it, we find the
    example that failed, and walk backward until we find a non-empty
    piece of explanatory text. That starts a block, and we output it
    in faux-markdown style until we get to the example that failed.
    """

    out = [self.DIVIDER]
    if test.filename:
        if test.lineno is not None and example.lineno is not None:
            lineno = test.lineno + example.lineno + 1
        else:
            lineno = '?'
        out.append('File "%s", line %s, in %s' %
                   (test.filename, lineno, test.name))
    else:
        out.append('Line %s, in %s' % (example.lineno + 1, test.name))

    example_idx = test._parsed.index(example)
    header_idx = example_idx
    while (header_idx > 0 and
           (isinstance(test._parsed[header_idx], doctest.Example) or
            test._parsed[header_idx] == '')):
        header_idx -= 1
    s = ""
    for i in range(header_idx, example_idx + 1):
        x = test._parsed[i]
        if isinstance(x, str):
            s += x
        else:
            s += ">>> " + x.source
            if x.want:
                s += x.want
    out.append(doctest._indent(s))
    return '\n'.join(out) + "\n"

def patch_doctest():
    doctest.DocTestRunner.report_unexpected_exception = patched_report_unexpected_exception
    doctest.DocTestRunner._failure_header = patched_failure_header
    doctest._SpoofOut.truncate = patched_truncate
    doctest.DocTestParser.parse = patched_parse
    doctest.DocTestParser.get_doctest = patched_get_doctest

def run_doctests(files):
    patch_doctest()
    mapped_results = dict()
    for fname in files:
        mapped_results[fname] = doctest.testfile(
            fname, optionflags=doctest.ELLIPSIS | doctest.REPORT_ONLY_FIRST_FAILURE)
    return mapped_results

def parse_arguments(argv):
    parser = argparse.ArgumentParser(description='WBE test runner')
    parser.add_argument("chapter",
                        nargs="?",
                        default=DEFAULT_CICD,
                        choices=list(CURRENT_TESTS),
                        help="Which chapter's tests to run")
    parser.add_argument("--index",
                        type=int,
                        help="Run the nth test from the chapter. "
                        "(Requires passing a full chapter name.)")
    args = parser.parse_args(argv[1:])

    return args

def main(argv):
    args = parse_arguments(argv)
    testkey = args.chapter
    if args.index is not None:
        assert args.chapter.startswith("chapter")
        testkey = args.chapter + "-" + str(args.index)

    tests = CURRENT_TESTS[testkey]

    mapped_results = run_doctests(tests)
    total_state = "all passed"
    print("\nSummarised results\n")
    for name, (failure_count, test_count) in mapped_results.items():
        state = "passed"
        if failure_count != 0:
            state = "failed {:<2} out of {:<2} tests".format(failure_count, test_count)
            total_state = "failed"
        print("{:>42}: {}".format(name, state))
    print("-" * 52)
    print("{:>42}: {} ".format("Final", total_state))

    return int(total_state == "failed")


if __name__ == "__main__":
    retcode = 130  # meaning "Script terminated by Control-C"

    try:
        retcode = main(sys.argv)
    except KeyboardInterrupt:
        print("")
        print("Goodbye")

    sys.exit(retcode)
