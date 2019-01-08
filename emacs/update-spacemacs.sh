#!/bin/bash
set -eux
cd ~/.emacs.d
git pull -p
rm -rf .cache
rm -rf elpa
