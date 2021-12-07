#!/bin/sh

jb build --all book/
ghp-import -n -p -f book/_build/html/
