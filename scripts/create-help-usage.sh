#!/usr/bin/env bash
PATH=".:matrix_commander/:$PATH" &&
    matrix-commander --usage >help.usage.txt
echo "help.usage.txt is $(wc -l help.usage.txt | cut -d ' ' -f1) lines long"
