from itertools import chain
from pathlib import Path
from subprocess import check_output, run, check_call

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

    # TODO pruning? 
