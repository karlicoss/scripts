from itertools import chain
from pathlib import Path
import re
from subprocess import check_output, run, check_call
from datetime import datetime
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


def do_borg(*, repo: Repo, paths, exclude=(), dry=False) -> None:
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


    def exists() -> bool:
        res = borg('info', repo, check=False)
        return res.returncode == 0


    if not exists():
        borg('init', '--encryption=none')

    # TODO how to keep options in sync?
    borg(
        'create',

        # ugh, stats are not allowed with dry
        *(
            ['--dry-run']
            if dry else
            [
                '--stats',
                '--filter', 'AME', # only list changes, exclude present files
            ]
        ),

        '--compression', 'lz4', # fast, not super efficient
        '--verbose',
        '--list',
        '--show-rc', # return code


        '--exclude-caches',
        '--exclude', '**/.dropbox.cache',

        # python
        '--exclude', '**/.mypy_cache',
        '--exclude', '**/.tox',

        '--exclude', '**/node_modules',

        '--exclude', '**/.stack-work', # haskell

        *chain.from_iterable(['--exclude', x] for x in exclude),

        '--exclude-if-present', '.rustc_info.json', # rust
        '--exclude-if-present', '.borg-exclude', # custom
        '--exclude-if-present', '.borgignore', # TODO eh, I guess it's more consistent than .borg-exclude
        "::{hostname}-{utcnow}",
        *paths,
    )

    dt = datetime.now()
    for p in paths:
        heartbeat(path=Path(p), repo=repo, dt=dt)

    # TODO pruning? 
