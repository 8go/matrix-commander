#!/usr/bin/env bash
PATH=".:matrix_commander/:$PATH" &&
    matrix-commander --help | grep -E "^  -" |  awk -F '  ' '{print $2}' | sort > help.short.txt
echo "help.short.txt is $(wc -l help.short.txt | cut -d ' ' -f1) lines long"

