#!/usr/bin/env python3
import os
from os.path import isdir, islink, exists, isfile, join, basename
from pathlib import Path

from enum import Enum
import sys

import logging
from kython import setup_logzero
from kython import PathIsh
from kython.fs import apply_on


class XX(Enum):
    BAIL = 'bail'
    REC  = 'recurse'


def traverse(root: PathIsh, handler, logger=None):
    if logger is None:
        logger = logging.getLogger('fs-traverse')
    for root, dirs, files in os.walk(root):
        res = handle(root, dirs, files) # TODO map to Path?
        if res == XX.BAIL:
            logger.info('skipping %s', root) # TODO reason would be nice?
            dirs[:] = []


def get_logger():
    return logging.getLogger('symlink-checker')


IGNORED_DIRS = [
    'node_modules',
]

# TODO eh, global variable...
broken = []

def handle(root, dirs, files) -> XX:
    logger = get_logger()
    if basename(root) in IGNORED_DIRS:
        return XX.BAIL
    if '.symlink-checker-ignore' in files:
        return XX.BAIL
    for f in files:
        ff = join(root, f)
        if islink(ff) and not exists(ff):
            broken.append(ff)
            logger.error(f"broken: {ff}")
    return XX.REC


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
