#!/usr/bin/env python

"""Tweet sentiment analysis."""

import MySQLdb
import pickle
import sys

from tweet import *

def read_all(phile):
    try:
        while True:
            yield pickle.load(phile)
    except EOFError:
        pass

if __name__ == '__main__':
    count = 0
    for tweet in read_all(sys.stdin):
        count += 1
    print count
