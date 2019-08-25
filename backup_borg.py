from pathlib import Path
from subprocess import check_output, run, check_call

def do_borg(repo, paths) -> None:
    repo = Path(repo)
    paths = list(map(str, paths))

    def borg(*args):
        run(
            ['borg', *args],
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
        '--compression', 'lz4', # fast, not super efficient
        '--verbose',
        '--filter', 'AME', # only list changes, exclude present files
        '--list',
        '--stats',
        '--show-rc', # return code


        '--exclude-caches',
        '--exclude', '**/.dropbox.cache',

        # python
        '--exclude', '**/.mypy_cache',
        '--exclude', '**/.tox',

        '--exclude', '**/node_modules',

        '--exclude', '**/.stack-work', # haskell

        '--exclude-if-present', '.rustc_info.json', # rust
        '--exclude-if-present', '.borg-exclude', # custom
        "::{hostname}-{utcnow}",
        *paths,
    )

    # TODO pruning? 
