#!/bin/sh

jb build --all book/
ghp-import -n -p -f book/_build/html/
git add . -A
git commit -m "$1"
git push origin master
