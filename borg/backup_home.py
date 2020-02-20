#!/usr/bin/env python3
from pathlib import Path

from backup_borg import do_borg

def do_borg_home(**kwargs):
    return do_borg(
        repo=str(Path(__file__).absolute().parent / 'home'),
        paths=['/home/karlicos'],
        exclude=['/home/karlicos/' + p for p in [
            '.borg-passphrase',

            '.cache/borg',
            '.cache/chromium',
            '.cache/go-build',
            '.cache/jedi',
            '.cache/mozilla',
            '.cache/pip',
           
            '.config/syncthing/index-*',

            '.recoll/xapiandb',


            '.dropbox',
            '.dropbox-dist*',

            '.cabal',
            '.cargo',
            '.gradle',
            '.npm',
            '.rustup',
            '.stack',

            '.local/lib',
            '.local/share/Trash',

            'snap/spotify',
 
            ## glumov, perm errors
            '.rnd',
            'postgres',
            ##
        ]], 
        **kwargs,
    )
