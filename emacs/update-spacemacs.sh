#!/bin/bash
set -eux


# check no emacs instances are running
! pgrep -a emacs || exit 1

cd ~/.emacs.d
rm -rf elpa

rm -rf .cache
mkdir .cache
ln -s ~/configs-nogit/emacs/places  .cache/places
ln -s ~/configs-nogit/emacs/recentf .cache/recentf

git pull -p


GDIR=~/.emacs.d/elpa/gnupg
# meh https://github.com/syl20bnr/spacemacs/issues/13054
mkdir -p "$GDIR"
gpg --homedir "$GDIR" --receive-keys 066DAFCB81E42C40
