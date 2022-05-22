#!/bin/bash

# tiny script to lint matrix-commander.py

FN="matrix-commander.py"

if ! [ -f "$FN" ]; then
    FN="../$FN"
    if ! [ -f "$FN" ]; then
        echo -n "ERROR: $(basename -- "$FN") not found. "
        echo "Neither in local nor in parent directory."
        exit 1
    fi
fi
isort "$FN" && flake8 "$FN" && python3 -m black --line-length 79 "$FN"
