#!/usr/bin/env python
"""
Sort Twitter URLs by the ID at the end,
the same as sorting chronologically.
Usage:
python sort_twitter_urls.py list_of_urls.txt
"""
from __future__ import print_function, unicode_literals
import fileinput

# from operator import itemgetter
# from pprint import pprint

if __name__ == "__main__":
    lines = [line.rstrip("\n").split("/") for line in fileinput.input()]

    # lines.sort(key=itemgetter(int(-1)))
    lines = sorted(lines, key=lambda i: int(i[-1]))

    for line in lines:
        print(line[-1])

    for line in lines:
        print("{0}".format("/".join(line)))

# End of file
