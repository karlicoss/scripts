#!/usr/bin/env python3
import os
from os.path import isdir, islink, exists, isfile, join
import sys

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('symlink-checker')

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
    # TODO do not walk inside...
    # but for now it's fine, works quick enough..
    for dp, dirs, files in os.walk(p):
        if '.check-symlinks' in files:
            check(dp)



for p in PATHS:
    go(p)


if len(broken) > 0:
    sys.exit(1)
