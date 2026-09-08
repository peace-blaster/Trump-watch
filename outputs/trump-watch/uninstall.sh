#!/bin/sh
set -eu
if [ "$#" -gt 1 ]; then echo "Usage: $0 [prefix]" >&2; exit 1; fi
prefix=${1:-"$HOME/.local"}
target="$prefix/bin/trump-watch"
if [ -L "$target" ]; then echo "Refusing to remove a symbolic link: $target" >&2; exit 1; fi
if [ -f "$target" ]; then
    if ! grep -q 'Trump watch: published YouGov approval tracker, standard library only.' "$target"; then
        echo "Refusing to remove an unrecognized file: $target" >&2; exit 1
    fi
    rm -- "$target"
    echo "Removed $target"
else
    echo "Already uninstalled: $target"
fi
echo 'Cached polling data is retained. See README for cache removal.'
