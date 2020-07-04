#!/usr/bin/env python3
from pathlib import Path

from backup_borg import do_borg

# todo not sure if should autodetect..
USER = 'karlicos'


def do_borg_home(**kwargs):
    REPO = str(Path(__file__).absolute().parent / 'home')
    return do_borg(
        repo=REPO,
        paths=[f'/home/{USER}'],
        # TODO reuse excludefrom file?
        # exclude=[f'/home/{USER}/' + p for p in [
        #     '.borg-passphrase',

        #     '.cache/borg',
        #     '.cache/chromium',
        #     '.cache/go-build',
        #     '.cache/jedi',
        #     '.cache/mozilla',
        #     '.cache/pip',
        #    
        #     TODO ugh. yet another argument for keeping it elsewhere...
        #     '.config/syncthing/index-*',

        #     '.recoll/xapiandb',


        #     '.dropbox',
        #     '.dropbox-dist*',

        #     '.cabal',
        #     '.cargo',
        #     '.gradle',
        #     '.npm',
        #     '.rustup',
        #     '.stack',

        #     '.local/lib',
        #     '.local/share/Trash',

        #     'snap/spotify',
 
        #     ## glumov, perm errors
        #     '.rnd',
        #     'postgres',
        #     ##
        # ]], 
        **kwargs,
    )
# TODO prune

if __name__ == '__main__':
    do_borg_home()

