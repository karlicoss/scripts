#!/usr/bin/env python3
import os
from os.path import isdir, islink, exists, isfile, join, basename
from pathlib import Path

import sys

import logging
from kython import setup_logzero
from kython.fs import Go, traverse


def get_logger():
    return logging.getLogger('symlink-checker')


IGNORED_DIRS = [
    'node_modules',
]

# TODO eh, global variable...
broken = []

def handle(root, dirs, files) -> Go:
    logger = get_logger()
    if basename(root) in IGNORED_DIRS:
        return Go.BAIL
    if '.symlink-checker-ignore' in files:
        return Go.BAIL
    for f in files:
        ff = join(root, f)
        if islink(ff) and not exists(ff):
            broken.append(ff)
            logger.error(f"broken: {ff}")
    return Go.REC


def main():
    logger = get_logger()
    setup_logzero(logger, level=logging.DEBUG)

    import argparse
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('root', nargs='+', type=Path)
    args = p.parse_args()

    for p in args.root:
        logger.info("checking %s", p)
        traverse(p, handle, logger=logger)

    if len(broken) > 0:
        sys.exit(1)

if __name__ == '__main__':
    main()
