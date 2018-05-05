#!/bin/bash
cd ~/.emacs.d
git pull -p
rm -rf .cache
rm -rf elpa
