from itertools import chain
from pathlib import Path
from subprocess import check_output, run, check_call
from datetime import datetime


def heartbeat(*, path: Path, repo: Path, dt: datetime):
    """
    Heartbeat so we know when was the last time directory was backed up
    """
    payload = f'''
{dt.timestamp()}
{dt.isoformat()}
'''.lstrip()
    hb_dir = path / '.borg-heartbeat'
    hb_dir.mkdir(exist_ok=True)

    # TODO disk label?
    mount = check_output(['df', repo]).decode('utf8').splitlines()[-1].split()[-1]
    mount = mount.replace('/', '_')
    (hb_dir / mount).write_text(payload)


def do_borg(*, repo, paths, exclude=(), dry=False) -> None:
    repo = Path(repo)
    paths = list(map(str, paths))

    def borg(*args):
        cmd = ['borg', *args]
        print(f"Running: {cmd}")
        run(
            cmd,
            check=True,
            env={
                'BORG_REPO': repo,
            },
        )

    if not repo.exists():
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
        "::{hostname}-{utcnow}",
        *paths,
    )

    dt = datetime.now()
    for p in paths:
        heartbeat(path=Path(p), repo=repo, dt=dt)

    # TODO pruning? 
