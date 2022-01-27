#!/bin/sh

jb build --all book/
cp book/figs/*.mp4 book/_build/html/
ghp-import -n -p -f book/_build/html/
git add . -A
git commit -m "$1"
git push origin master
