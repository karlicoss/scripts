#!/usr/bin/env python3
import argparse
import difflib
import logging
import os.path
import sys

from kython import atomic_write, get_logzero

logger = get_logzero("DiffMonitor", level=logging.INFO)

# TODO so it should take stdin?

def load_state(path: str):
    if os.path.lexists(path):
        with open(path, 'r') as fo:
            return fo.read()
    else:
        return None

def save_state(path: str, value: str):
    with atomic_write(path, 'w') as fo:
        fo.write(value)


# TODO difflib?

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", help="Previous state file", required=True)
    # TODO tag for logger?
    # TODO rotating state files?

    args = parser.parse_args()


    prev_state = load_state(args.state)
    cur_state = sys.stdin.read()
    if prev_state is None:
        logger.warn("No previous state")
        save_state(args.state, cur_state)
    elif prev_state == cur_state:
        logger.info("States match")
    else:
        logger.error("States differ!!!!")
        diff = difflib.context_diff(prev_state.splitlines(), cur_state.splitlines())
        logger.error("Diff:")
        for d in diff:
            logger.error(d)
        save_state(args.state, cur_state)
        sys.exit(1)


if __name__ == "__main__":
    main()
