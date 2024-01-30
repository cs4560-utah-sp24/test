#!/usr/bin/env python3

import os
import sys
import json

def summarize(data):
    s = ""
    s += "| Test file | Failed | Total |\n"
    s += "|---|---|---|\n"
    grade = 0
    for name, (failure_count, test_count) in data:
        if failure_count:
            s += f"| `{name}` | {failure_count} | {test_count} |\n"
        else:
            s += f"| `{name}` | \N{White heavy check mark} | {test_count} |\n"
        if test_count > 0:
            grade += 1 - failure_count / test_count
        else:
            grade += 1
    s += "\n"
    s += "**Overall Grade**: " + str(round(grade * 10)) + "/50\n"
    print(s)
    
if __name__ == "__main__":
    data = json.load(open("test/gh.json"))
    summarize(data)

