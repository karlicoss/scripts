#!/usr/bin/env python3
import argparse
import difflib
import logging
import os.path
import subprocess
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", help="Previous state file", required=True)
    parser.add_argument("-i", action='store_true', default=False, help="Listen for stdin")
    parser.add_argument('command', nargs='*')
    # TODO tag for logger?
    # TODO rotating state files?

    args = parser.parse_args()


    prev_state = load_state(args.state)

    cur_state: str
    if args.i:
        cur_state = sys.stdin.read()
    else:
        cur_state = subprocess.check_output(args.command).decode('utf-8')

    exitcode = 0
    if prev_state is None:
        logger.warn("No previous state")
    elif prev_state == cur_state:
        logger.info("States match")
    else:
        logger.error("States differ!!!!")
        diff = difflib.context_diff(prev_state.splitlines(), cur_state.splitlines())
        logger.error("Diff:")
        for d in diff:
            logger.error(d)
        exitcode = 1
    save_state(args.state, cur_state)
    sys.exit(exitcode)

if __name__ == "__main__":
    main()
