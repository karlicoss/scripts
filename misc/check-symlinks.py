#!/usr/bin/env python3
import os

from os.path import isdir, islink, exists, isfile, join, basename
from pathlib import Path
from fnmatch import fnmatch

import sys

import logging
from kython import setup_logzero
from kython.fs import Go, traverse

from typing import Sequence, Optional, Dict, Any


def get_logger():
    return logging.getLogger('symlink-checker')

# TODO eh, global variable...
broken = []


def load_gitignore(path: Path, sroot: Path):
    # shit. tried using pip install gitignore_parser, but it's got a bug that doesn't allow using '*'...
    # this format is a subset and only supports ignored files
    try:
        lines = [l for l in list(path.read_text().splitlines()) if len(l.strip()) > 0]
        root = path.parent
        def check(p: Path, sroot=sroot):
            # TODO check should be defensive too?
            relp = str(p.relative_to(sroot))
            for pat in lines:
                if fnmatch(relp, pat):
                    return True
            return False
        return check
    except Exception as e:
        logger = get_logger()
        logger.exception(e)
        logger.error('while loading %s; fallback to empty ignore file', path)
        return lambda x: False


# TODO shit, that sucks and a bit too slow;
# I just was too annoyed at trying to make it pass ignorefile recursively
ignores: Dict[Path, Any] = {}

def ignored(path: Path):
    # TODO that really, really sucks...
    # shit, that's just ridiculously slow
    cur = path
    while cur != cur.parent:
        cur = cur.parent
        if cur in ignores:
            return ignores[cur](path)

    return False


# TODO messy...
def load_scignore(root: Path, files: Sequence[str], sroot: Optional[Path]=None):
    if sroot is None:
        sroot = root
    for p in ('.scignore', '.symlink-checker.ignore'):
        if p in files:
            ignores[sroot] = load_gitignore(root / p, sroot=sroot)
            return


def handle(root, dirs, files):
    root = Path(root)
    logger = get_logger()

    if ignored(root):
        logger.info('ignored: %s', root)
        return Go.BAIL

    load_scignore(root, files)


    for f in files:
        ff = root / f
        if ignored(ff):
            logger.info('ignored: %s', ff)
        elif ff.is_symlink() and not ff.exists():
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


    # TODO somewhat hacky..
    home = Path('~').expanduser()
    load_scignore(home, [p.name for p in home.iterdir()], sroot=Path('/'))

    # TODO might be good to handle errors gracefully in case of bad gitignore
    for p in [p.absolute() for p in args.root]:
        logger.info("checking %s", p)
        traverse(p, handle, logger=logger)

    if len(broken) > 0:
        sys.exit(1)

if __name__ == '__main__':
    main()
