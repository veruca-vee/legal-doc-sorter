#!/bin/sh
# Thin wrapper for Linux / macOS / Termux. The real work is sort_docs.py.
exec python3 "$(dirname "$0")/sort_docs.py" "$@"
