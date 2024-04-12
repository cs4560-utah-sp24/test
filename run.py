#!/usr/bin/env python3


import argparse
import doctest
import os
import sys
import re
import datetime
import tests.wbemocks as wbemocks
import json
import multiprocessing

sys.path.append(os.getcwd())

MST = datetime.timezone(datetime.timedelta(hours=-7), "MST")
MDT = datetime.timezone(datetime.timedelta(hours=-6), "MDT")
GH_JSON_PATH = "test/gh.json"

CHAPTER_DEADLINES = {
    "ch01": datetime.datetime(2024, 1, 29, tzinfo=MST),
    "ch02": datetime.datetime(2024, 2,  5, tzinfo=MST),
    "ch03": datetime.datetime(2024, 2, 12, tzinfo=MST),
    "ch04": datetime.datetime(2024, 2, 19, tzinfo=MST),
    "ch05": datetime.datetime(2024, 2, 26, tzinfo=MST),
    "ch06": datetime.datetime(2024, 3,  4, tzinfo=MST),
    # Spring break
    "ch07": datetime.datetime(2024, 3, 18, tzinfo=MDT),
    "ch08": datetime.datetime(2024, 3, 25, tzinfo=MDT),
    "ch09": datetime.datetime(2024, 4,  1, tzinfo=MDT),
    "ch10": datetime.datetime(2024,4,  8, tzinfo=MDT),
}

def get_current_chapter():
    chapter = min([
        (chapter, deadline)
        for chapter, deadline in CHAPTER_DEADLINES.items()
        if datetime.datetime.now(datetime.timezone.utc) <= deadline
    ], default=None, key=lambda x: x[1])

    if chapter:
        return chapter[0]
    else:
        print("WARNING: No chapters outstanding, using chapter10", file=sys.stderr)
        return list(CHAPTER_DEADLINES)[-1] # Depends on sorted dictionaries


CURRENT_TESTS = {
    "ch01": ["base.md",
             "ex-http-11.md",
             "ex-file-urls.md",
             "ex-redirects.md",
             "ex-caching.md",
             ],
    "ch02": ["base.md",
             "ex-line-breaks.md",
             "ex-resizing.md",
             "ex-scrollbar.md",
             "ex-emoji.md",
             ],
    "ch03": ["base.md",
             "ex-centered-text.md",
             "ex-superscripts.md",
             "ex-soft-hyphens.md",
             "ex-small-caps.md",
             ],
    "ch04": ["base.md",
             "ex-comments.md",
             "ex-paragraphs.md",
             "ex-scripts.md",
             "ex-quoted-attributes.md",],
    "ch05": ["base.md",
             "ex-hidden-head.md",
             "ex-bullets.md",
             "ex-links-bar.md",
             "ex-anonymous-boxes.md",
             ],
    "ch06": ["base.md",
             "ex-fonts.md",
             "ex-width-height.md",
             "ex-class-selectors.md",
             "ex-shorthand-properties.md",
             ],
    "ch07": ["base.md",
             "ex-backspace.md",
             "ex-middle-click.md",
             "ex-fragments.md",
             "ex-bookmarks.md",
             ],
    "ch08": ["base.md",
             "ex-enter-key.md",
             "ex-check-boxes.md",
             "ex-get-forms.md",
             "ex-rich-buttons.md",
             ],
    "ch09": ["base.md",
             "ex-create-element.md",
             "ex-node-children.md",
             "ex-ids.md",
             "ex-event-bubbling.md",
             ],
    "ch10": ["base.md",
             "ex-new-inputs.md",
             "ex-certificate-errors.md",
             "ex-script-access.md",
             "ex-referer.md",
             ],
}

REPORT_FIRST_ERROR = False
REPORT_DIFF = False

# Below this are a variety of "fixes" to doctest that make it more user-friendly

old_truncate = doctest._SpoofOut.truncate

def patched_truncate(self, size=None):
    """
    Patch the fake doctest stdout to save the output long enough to use when reporting errors
    """
    self._old_getvalue = self.getvalue()
    old_truncate(self, size)

def patched_report_failure(self, out, test, example, got):
    """
    Patch the failure printer to record the current example so we can
    count failures on a block, not line basis.
    """

    test._failed_examples.append(example)
    if REPORT_FIRST_ERROR and len(test._failed_examples) > 1: return

    out(self._failure_header(test, example) +
        self._checker.output_difference(example, got, self.optionflags))


def patched_report_unexpected_exception(self, out, test, example, exc_info):
    """
    Patch the doctest printer to print output when exceptions occur.

    Note that this uses the _old_getvalue saved above, which doctest otherwise throws out
    when exceptions are thrown.
    """
    test._failed_examples.append(example)
    if REPORT_FIRST_ERROR and len(test._failed_examples) > 1: return

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

    Also set up the failed_examples list.
    """
    out = old_get_doctest(self, string, globs, name, filename, lineno)
    out._parsed = self._parsed
    out._failed_examples = []
    return out

old_check_output = doctest.OutputChecker.check_output

def patched_check_output(self, want, got, optionflags):
    """
    Strips all debug lines out from `got` before checking output. By
    stripping them here but not in output_difference, we end up
    calling debug-only diffs a successful result, but still print the
    output when the diff has non-debug-only lines.
    """
    got_no_debug = "\n".join([
        line for line in
        got.split("\n")
        if not line.startswith("!dbg")
    ])
    return old_check_output(self, want, got_no_debug, optionflags)

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
            s += ">>> " + "\n... ".join(x.source.strip("\n").split("\n")) + "\n"
            if x.want and i != example_idx:
                s += x.want
    out.append(doctest._indent(s))
    return '\n'.join(out) + "\n"

LAST_TEST_RESULT = None

old_record_outcome = doctest.DocTestRunner._DocTestRunner__record_outcome

def patched_record_outcome(self, test, failures, tries, skips=None):
    """
    Compute failures and successes on a per-block basis.
    """

    all_failures = set(test._failed_examples)
    idx = 0
    passed_blocks = 0
    failed_blocks = 0
    while idx < len(test._parsed):
        assert isinstance(test._parsed[idx], str) and test._parsed[idx] != ''
        idx += 1
        did_fail = False
        while idx < len(test._parsed):
            if isinstance(test._parsed[idx], str) and test._parsed[idx] != '':
                break
            elif isinstance(test._parsed[idx], doctest.Example):
                did_fail = did_fail or (test._parsed[idx] in all_failures)
            idx += 1

        if did_fail:
            failed_blocks += 1
        else:
            passed_blocks += 1
    
    global LAST_TEST_RESULT
    LAST_TEST_RESULT = (failed_blocks, failed_blocks + passed_blocks)
    skips_arg = [] if skips is None else [skips]
    return old_record_outcome(self, test, failed_blocks, passed_blocks + failed_blocks, *skips_arg)

def patch_doctest():
    doctest.DocTestRunner.report_failure = patched_report_failure
    doctest.DocTestRunner.report_unexpected_exception = patched_report_unexpected_exception
    doctest.DocTestRunner._failure_header = patched_failure_header
    doctest.OutputChecker.check_output = patched_check_output
    doctest._SpoofOut.truncate = patched_truncate
    doctest.DocTestParser.parse = patched_parse
    doctest.DocTestParser.get_doctest = patched_get_doctest
    doctest.DocTestRunner._DocTestRunner__record_outcome = patched_record_outcome

def run_doctests(files):
    global LAST_TEST_RESULT
    patch_doctest()
    mapped_results = dict()
    sys.modules["wbemocks"] = wbemocks
    flags = doctest.ELLIPSIS | doctest.IGNORE_EXCEPTION_DETAIL
    if REPORT_DIFF: flags |= doctest.REPORT_NDIFF
    for fname in files:
        fname_abs = os.path.join(os.path.dirname(__file__), fname)
        doctest.testfile(fname_abs, module_relative=False, optionflags=flags)
        mapped_results[fname] = LAST_TEST_RESULT
        LAST_TEST_RESULT = None
    return mapped_results

def parse_arguments(argv):
    parser = argparse.ArgumentParser(description='WBE test runner')
    parser.add_argument("chapter",
                        nargs="?",
                        default="current",
                        help="Which chapter's tests to run")
    parser.add_argument("--index",
                        type=int,
                        help="Run the nth test from the chapter. "
                        "(Requires passing a full chapter name.)")

    # Control over output
    parser.add_argument(
        "--all", action="store_true",
        help="Run all the tests, instead of stopping at the first failure.")
    parser.add_argument(
        "--diff", action="store_true",
        help="Show a line-by-line diff between expected and actual output")

    # Control over test configuration
    parser.add_argument(
        '-b', '--browser_path',
        help='Directory containing browser.py'),

    # Control over uploader
    parser.add_argument(
        "--no-upload", action="store_true",
        help="Do not upload a copy of the code to the instructor")

    # Control over GH mode
    parser.add_argument(
        "--gh", action="store_true",
        help=f"Write results to {GH_JSON_PATH} (for generating grade summaries)")
    parser.add_argument(
        "--ghsetup", action="store_true",
        help="Output environment variables for Github CI script")
    args = parser.parse_args(argv[1:])

    return args

def ghsetup(tests):
    assert os.getenv("GITHUB_ENV"), "Cannot execute gh subcommand without GITHUB_ENV set"
    with open(os.getenv("GITHUB_ENV"), "a") as ghenv:
        ghenv.write(f"HWPARTS={len(tests)}\n")
        for i, test in enumerate(tests):
            fname_abs = os.path.join(os.path.dirname(__file__), "tests", test)
            name = open(fname_abs).readline()
            name = name.removeprefix("Tests for WBE")
            ghenv.write(f"HWPART{i+1}={name}\n")
    print("Saved Github information in environment variables")
    if os.path.isfile(GH_JSON_PATH):
        os.unlink(GH_JSON_PATH)
    return 0

def upload_py(testkey):
    if not os.path.exists("browser.py"):
        print("ERROR: no `browser.py` file found", file=sys.stderr)
        sys.exit(1)

    # macOS issue with threads
    os.environ["no_proxy"] = "*"

    all_modules = set(sys.modules.keys())
    import browser
    if os.path.exists("server.py"): import server
    new_modules = set(sys.modules.keys()) - all_modules
    browser_path = os.path.realpath(browser.__file__)
    files = []

    base_path = os.path.dirname(browser_path)
    for module_name in new_modules:
        module = sys.modules[module_name]
        if not hasattr(module, "__file__"): continue
        module_path = os.path.realpath(module.__file__)
        try:
            if os.path.commonpath([module_path, base_path]) == base_path:
                files.append(module_path)
        except ValueError:
            continue

    git_path = os.path.join(base_path, ".git", "config")
    student = "unknown"
    if os.path.isfile(git_path):
        in_remote = False
        with open(git_path) as f:
            for line in f:
                if line == "[remote \"origin\"]\n":
                    in_remote = True
                elif line.startswith("["):
                    in_remote = False
                elif in_remote and "cs4560-utah-sp24" in line:
                    student = line.strip().rsplit("/", 1)[1]
                    if student.endswith(".git"):
                        student = student[:-4] # Remove the extension
                    break
    student = "".join([
        char if char.isalnum() or char in "-_" else "-"
        for char in student
    ])

    fname = f"{student}-{testkey}-{datetime.datetime.now():%Y-%m-%d-%H-%M-%S-%f}.tgz"
    import tarfile

    tar_path = os.path.realpath("test/src.tgz")
    try:
        with tarfile.open(tar_path, "x:gz") as f:
            for path in files:
                f.add(path, arcname=path.removeprefix(base_path),
                      recursive=False)
        with open(tar_path, "rb") as f:
            data = f.read()
    finally:
        os.unlink(tar_path)

    # Don't use SSL because one student had issues with that
    url = f"http://browser.engineering/api/savefile/"
    import urllib.request, urllib.error
    # Based on https://gist.github.com/AhnMo/be8cc21bf02c9e92247d74d460727ce0
    boundary = b"wbe"
    while boundary in data: boundary.append(boundary)

    contents  = f"--{boundary}\r\n".encode("ascii")
    contents += f'Content-Disposition: form-data; name="file"; filename="{fname}"\r\n'.encode("ascii")
    contents += b'Content-Type: application/gzip\r\n'
    contents += b"\r\n"
    contents += data

    content_type = f"multipart/form-data; boundary={boundary}".encode("ascii")

    req = urllib.request.Request(url, data=contents, headers={
        "Content-Type": content_type,
    }, method="POST")
    try:
        out = urllib.request.urlopen(req)
        if out.status == 200:
            return
        else:
            msg = out.read()
    except urllib.error.URLError as e:
        msg = e.read().decode("latin1")
    
    print(f"ERROR: upload failed because {msg}, continuing", file=sys.stderr)

def get_tests(testkey):
    if testkey == "all":
        return sum([get_tests(chname) for chname in CURRENT_TESTS], [])

    if "-" in testkey:
        chapter, ex = testkey.split("-", 1)
    elif testkey.isdigit():
        chapter, ex = get_current_chapter(), testkey
    elif testkey in CURRENT_TESTS:
        chapter, ex = testkey, "all"
    elif testkey == "current":
        chapter, ex = get_current_chapter(), "all"

    assert chapter in CURRENT_TESTS, f"Unknown chapter {chapter}"
    chapter_tests = [
        os.path.join(chapter, testname)
        for testname in CURRENT_TESTS[chapter]
    ]

    if ex == "all":
        return chapter_tests
    elif ex.isdigit():
        assert 0 < int(ex) <= 5, f"Invalid test index {ex} in {chapter} (1-5 allowed)"
        return [chapter_tests[int(ex) - 1]]
    else:
        ex_name = "base.md" if ex == "base" else "ex-" + ex + ".md"
        ex_file = os.path.join(chapter, ex_name)
        assert ex_file in chapter_tests, f"Unknown test {ex} in {chapter}"
        return [ex_file]

def main(argv):
    args = parse_arguments(argv)

    testkey = args.chapter
    tests = get_tests(testkey)

    bpath = args.browser_path
    sys.path.append(bpath)
    upload_proc = None
    if not (args.no_upload or args.ghsetup):
        upload_proc = multiprocessing.Process(target=upload_py, args=(testkey,))
        upload_proc.start()

    if args.ghsetup:
        ghsetup(tests)
        return 0

    global REPORT_FIRST_ERROR, REPORT_DIFF
    REPORT_FIRST_ERROR = not args.gh and not args.all
    REPORT_DIFF = args.diff
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

    if args.gh:
        ALL_TESTS = CURRENT_TESTS[testkey.split("-", 1)[0]]
        if os.path.isfile(GH_JSON_PATH):
            current_data = json.load(open(GH_JSON_PATH))
        else:
            current_data = []
        current_data = [t for t in current_data if t[0] in ALL_TESTS]
        res = sorted(current_data + list(mapped_results.items()),
                     key=lambda a: ALL_TESTS.index(a[0]))
        with open(GH_JSON_PATH, "w") as f:
            json.dump(res, f)

    if upload_proc:
        if upload_proc.is_alive():
            # Give the upload 0.25s to complete before complaining
            upload_proc.join(.25)
        if upload_proc.is_alive():
            print("LOG: Waiting on upload to complete; feel free to kill with Ctrl-C")
            upload_proc.join()

    return int(total_state == "failed")


if __name__ == "__main__":
    retcode = 130  # meaning "Script terminated by Control-C"

    try:
        retcode = main(sys.argv)
    except KeyboardInterrupt:
        print("")
        print("Goodbye")

    sys.exit(retcode)
