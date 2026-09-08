#!/bin/sh
set -eu
# Trump watch installer v1
if [ "$#" -gt 1 ]; then echo "Usage: $0 [prefix]" >&2; exit 1; fi
prefix=${1:-"$HOME/.local"}
command -v python3 >/dev/null 2>&1 || { echo 'Python 3.8+ is required.' >&2; exit 1; }
python3 -c 'import sys; sys.exit(sys.version_info < (3,8))' || { echo 'Python 3.8+ is required.' >&2; exit 1; }
source_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
mkdir -p "$prefix/bin"
target="$prefix/bin/trump-watch"
if [ -e "$target" ] || [ -L "$target" ]; then
    echo "Refusing to overwrite $target; uninstall the existing copy first." >&2
    exit 1
fi
cp "$source_dir/trump-watch" "$target"
chmod 755 "$target"
echo "Installed $target"
echo "Run: $target"
echo "Add $prefix/bin to PATH if needed."
