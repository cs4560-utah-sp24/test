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
    "chapter1": datetime.datetime(2024, 1, 29, tzinfo=MST),
    "chapter2": datetime.datetime(2024, 2,  5, tzinfo=MST),
    "chapter3": datetime.datetime(2024, 2, 12, tzinfo=MST),
    "chapter4": datetime.datetime(2024, 2, 19, tzinfo=MST),
    "chapter5": datetime.datetime(2024, 2, 26, tzinfo=MST),
    "chapter6": datetime.datetime(2024, 3,  4, tzinfo=MST),
    "chapter7": datetime.datetime(2024, 3, 11, tzinfo=MDT),
    "chapter8": datetime.datetime(2024, 3, 18, tzinfo=MDT),
    "chapter9": datetime.datetime(2024, 3, 25, tzinfo=MDT),
    "chapter10": datetime.datetime(2024,4,  1, tzinfo=MDT),
}

def getCurrentChapter():
    chapter = min([
        (chapter, deadline)
        for chapter, deadline in CHAPTER_DEADLINES.items()
        if datetime.datetime.now(datetime.timezone.utc) <= deadline
    ], default=None, key=lambda x: x[1])

    if chapter:
        return chapter[0]
    else:
        print("WARNING: No chapters outstanding, using chapter10", file=sys.stderr)
        return "chapter10"


DEFAULT_CICD = getCurrentChapter()

CURRENT_TESTS = {
    "chapter1": ["chapter1-base-tests.md",
                 "chapter1-exercise-http-1-1-tests.md",
                 "chapter1-exercise-file-urls-tests.md",
                 "chapter1-exercise-redirects-tests.md",
                 "chapter1-exercise-caching-tests.md",
                 ],
    "chapter2": ["chapter2-base-tests.md",
                 "chapter2-exercise-line-breaks-tests.md",
                 "chapter2-exercise-resizing-tests.md",
                 "chapter2-exercise-scrollbar-tests.md",
                 "chapter2-exercise-emoji-tests.md",
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
                 "chapter5-exercise-links-bar-tests.md",
                 "chapter5-exercise-anonymous-boxes-tests.md",
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
                 "chapter8-exercise-get-forms-tests.md",
                 "chapter8-exercise-rich-buttons-tests.md",
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

REPORT_FIRST_ERROR = False

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
    doctest._SpoofOut.truncate = patched_truncate
    doctest.DocTestParser.parse = patched_parse
    doctest.DocTestParser.get_doctest = patched_get_doctest
    doctest.DocTestRunner._DocTestRunner__record_outcome = patched_record_outcome

def run_doctests(files):
    global LAST_TEST_RESULT
    patch_doctest()
    mapped_results = dict()
    sys.modules["wbemocks"] = wbemocks
    flags = doctest.ELLIPSIS
    for fname in files:
        fname_abs = os.path.join(os.path.dirname(__file__), "tests", fname)
        doctest.testfile(fname_abs, module_relative=False, optionflags=flags)
        mapped_results[fname] = LAST_TEST_RESULT
        LAST_TEST_RESULT = None
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
    parser.add_argument("--gh", action="store_true",
                        help="Write results to " + GH_JSON_PATH +
                        "(For generating grade summaries)")
    parser.add_argument("--ghsetup", action="store_true",
                        help="Output environment variables for Github")
    parser.add_argument("--no-upload", action="store_true",
                        help="Do not upload a copy of the code to the instructor")
    parser.add_argument('-b', '--browser_path', help='Directory containing browser.py')
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

def main(argv):
    args = parse_arguments(argv)

    testkey = args.chapter
    if args.index is not None:
        assert args.chapter.startswith("chapter")
        testkey = args.chapter + "-" + str(args.index)

    tests = CURRENT_TESTS[testkey]
    bpath = args.browser_path
    sys.path.append(bpath)
    upload_proc = None
    if not (args.no_upload or args.ghsetup or args.gh):
        upload_proc = multiprocessing.Process(target=upload_py, args=(testkey,))
        upload_proc.start()

    if args.ghsetup:
        ghsetup(tests)
        return 0

    global REPORT_FIRST_ERROR
    REPORT_FIRST_ERROR = not args.gh
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
