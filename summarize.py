#!/usr/bin/env python3

import os
import sys
import json

def summarize(data):
    s = ""
    s += "| Test file | Failed | Total |"
    s += "|---|---|---|"
    grade = 0
    for name, (failure_count, test_count) in data:
        s += f"| `{name}`, {failure_count} | {test_count} |"
        if test_count > 0:
            grade += 1 - failure_count / test_count
        else:
            grade += 1
    s += "Overall Grade: " + str(round(grade * 10)) + "/50"
    print(s)
    
if __name__ == "__main__":
    data = json.load(open("gh.json"))
    summarize(data)

