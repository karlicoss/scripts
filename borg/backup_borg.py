from itertools import chain
from pathlib import Path
import re
from subprocess import check_output, run, check_call
from datetime import datetime
from typing import Optional
import socket

# not necessarily a Path, e.g. could be ssh
Repo = str

def heartbeat(*, path: Path, repo: Repo, dt: datetime):
    """
    Heartbeat so we know when was the last time directory was backed up
    """
    payload = f'''
{dt.timestamp()}
{dt.isoformat()}
'''.lstrip()
    hb_dir = path / '.borg-heartbeat'
    hb_dir.mkdir(exist_ok=True)

    if '@' in repo: # must be remote
        label = re.sub(r'[^\w_.)( -]', '', repo)
    else:
        # TODO disk label?
        mount = check_output(['df', repo]).decode('utf8').splitlines()[-1].split()[-1]
        label = mount.replace('/', '_')
    (hb_dir / label).write_text(payload)


def do_borg(*, repo: Repo, paths, exclude=(), dry=False, compression=None, create_args=(), prune: Optional[str]=None) -> None:
    # TODO assert that paths exist? to prevent passing a single string...
    assert not isinstance(paths, str)
    paths = list(map(str, paths))

    def borg(*args, check=True):
        cmd = ['borg', *args]
        print(f"Running: {cmd}")
        return run(
            cmd,
            check=check,
            env={
                'BORG_REPO': repo,
            },
        )


    excludes = Path(__file__).resolve().absolute().parent / 'excludefrom'
    assert excludes.exists(), excludes

    def exists() -> bool:
        res = borg('info', repo, check=False)
        return res.returncode == 0


    if not exists():
        borg('init', '--encryption=none')

    # TODO copy pasta from quickborg script...
    mdry = [
        '--dry-run'
    ] if dry else [
        '--stats', # incompatible with dry
    ]

    # TODO how to keep options in sync?
    res = borg(
        'create',

        *mdry,
        *([] if dry else ['--filter', 'AME']), # only list changes, exclude present files
        '--compression', compression or 'lz4', # lz4 is fast, not super efficient
        '--verbose',
        '--list',
        '--show-rc', # return code


        '--exclude-caches',
        '--exclude-if-present', '.borgignore',
        '--exclude-from', str(excludes),
        *chain.from_iterable(['--exclude', x] for x in exclude),
        *create_args,

        "::{hostname}-{utcnow}",
        *paths,
        check=False,
    )
    if res.returncode > 0:
        # eh. might happen if there are permission issues...
        input('Borg exited with non-zero code! ctrl-c if you want to interrupt.')

    dt = datetime.now()
    for p in paths:
        if not dry:
            heartbeat(path=Path(p), repo=repo, dt=dt)

    # todo maybe ls or something?
    if prune is not None:
        borg(
            'prune',
            '-v',
            '--list',
            *mdry,
            *prune.split(),
        )
