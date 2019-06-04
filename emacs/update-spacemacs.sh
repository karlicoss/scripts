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
