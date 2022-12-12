#!/usr/bin/env bash
PATH=".:matrix_commander/:$PATH" &&
    matrix-commander --help >help.help.txt
echo "help.help.txt is $(wc -l help.help.txt | cut -d ' ' -f1) lines long"
