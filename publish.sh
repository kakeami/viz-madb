#!/bin/sh

jb build --all mynewbook/
ghp-import -n -p -f mynewbook/_build/html/
