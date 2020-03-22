#!/usr/bin/env python3
'''
Checks that everything on the filesystem is backed up somewhere: cloud/hard drives/etc
'''

from argparse import ArgumentParser
import os
from pathlib import Path
import sys
from typing import Optional, Set, List, Tuple

from kython.klogging2 import LazyLogger


logger = LazyLogger('crawl-dangling')


Reason = str
Handled = List[Tuple[Path, Reason]]

HANDLED: Handled = []


def load_config(config: Path):
    global HANDLED

    globs = {}  # type: ignore
    exec(config.read_text(), globs)

    HANDLED = globs['HANDLED']


# TODO use something more efficient? regex?
def matches_prefix(path: Path) -> bool:
    for p, reason in HANDLED:
        try:
            path.relative_to(Path(p))
            # TODO use reason?
            return True
        except ValueError:
            continue
    else:
        return False


def in_config(path: Path) -> bool:
    return matches_prefix(path=path)


def excluded(p: Path) -> bool:
    # TODO use .danglignignore file?
    if (p / '.nodangling').exists():
        return True
    return False


def main():
    p = ArgumentParser()
    p.add_argument('--config', type=Path, required=True)
    p.add_argument('roots', nargs='*')
    args = p.parse_args()

    config = args.config
    load_config(config)

    roots = [Path(p) for p in args.roots]
    assert len(roots) > 0  # sanity check

    errors = []
    def error(*args):
        logger.error(*args)
        errors.append(args)

    def is_handled(p: Path) -> bool:
        if in_config(p):
            return True
        if excluded(p):
            return True
        return False

    for dd in roots:
        logger.info('checking %s', dd)
        if not dd.exists():
            error("%s doesn't exist!", dd)
            continue
        for root, dirs, files in os.walk(dd, topdown=True):
            r = Path(root)
            logger.debug('checking %s', r)
            if is_handled(r):
                logger.info('skipping %s', r)
                dirs[:] = []
                files[:] = []
            for f in files:
                mf: Optional[Path] = None
                mf = r.joinpath(f)
                if mf is not None and not excluded(mf):
                    error(mf)

    if len(errors) > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
