#!/usr/bin/env bash

# tiny script to lint matrix_commander.py

FN="matrix_commander.py"

if ! [ -f "$FN" ]; then
    FN="matrix_commander/$FN"
    if ! [ -f "$FN" ]; then
        echo -n "ERROR: $(basename -- "$FN") not found. "
        echo "Neither in local nor in child directory."
        exit 1
    fi
fi
isort "$FN" && flake8 "$FN" && python3 -m black --line-length 79 "$FN"
