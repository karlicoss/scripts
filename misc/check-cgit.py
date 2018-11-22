#!/usr/bin/env python3
from subprocess import check_call, run
from os import listdir
from os.path import join, expanduser
import sys
from typing import Set

from kython.fs import apply_on


found: Set[str] = set()
cgit_tags = set(sorted(listdir(expanduser('~/.cgit'))))
error = False

def check(d: str):
    global error
    # ok, this it a cgit repo, let's find out if it's relevant to this computer..
    maybe_tags = set(listdir(join(d, '.cgit')))
    ints = maybe_tags.intersection(cgit_tags)
    if len(ints) == 0:
        print("ignoring " + d)
        return
    elif len(ints) > 1:
        print("too many tags matched in {}: {}".format(d, cgit_tags))
        error = True
        return
    ctag = next(iter(ints))
    if ctag in found:
        print("tag already processed " + ctag)
        error = True
        return

    found.add(ctag)

    print("checking " + d)
    res = run([
        'cgit', '--git-dir', join(d, '.git'), 'diff', '--shortstat', '--exit-code',
    ])
    if res.returncode > 0:
        error = True

def predicate(d, dirs, files):
    return '.cgit' in dirs

apply_on(predicate, '/L', check)


if error:
    sys.exit(1)
