#!/usr/bin/env python3
import os
from os.path import isdir, islink, exists, isfile, join
import sys

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('symlink-checker')

from kython.fs import apply_on

PATHS = [
   '/L/',
]

broken = []

def check(p):
    logger.info(f"checking {p}")
    for dp, dirs, files in os.walk(p):
        for f in files:
            ff = join(dp, f)
            if islink(ff) and not exists(ff):
                broken.append(ff)
                logger.error(f"broken: {ff}")


def go(p, recursive=False):
    for dp, dirs, files in os.walk(p):
        if '.check-symlinks' in files:
            check(dp)


def predicate(d, dirs, files):
    return '.check-symlinks' in files

for p in PATHS:
    apply_on(predicate, p, check)


if len(broken) > 0:
    sys.exit(1)
