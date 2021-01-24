#!/usr/bin/env python3
from pathlib import Path

from backup_borg import do_borg

# todo not sure if should autodetect..
USER = 'karlicos'


def do_borg_home(**kwargs) -> None:
    REPO = str(Path(__file__).absolute().parent / 'home')
    return do_borg(
        repo=REPO,
        paths=[f'/home/{USER}'],
        # see https://borgbackup.readthedocs.io/en/stable/usage/prune.html
        prune='--keep-within=30d --keep-monthly=-1',
        **kwargs,
    )
# TODO prune

if __name__ == '__main__':
    do_borg_home()

