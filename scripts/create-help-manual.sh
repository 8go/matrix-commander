#!/usr/bin/env bash
PATH=".:matrix_commander/:$PATH" &&
    matrix-commander --manual >help.manual.txt
echo "help.manual.txt is $(wc -l help.manual.txt | cut -d ' ' -f1) lines long"

# PATH=".:matrix_commander/:$PATH" &&
#     old_width=$(stty size | cut -d' ' -f2-) &&
#     stty cols 79 && matrix-commander --help >help.manual.txt &&
#     stty cols $old_width &&
#     stty size &&
#     echo -n "Max width: " &&
#     wc -L help.manual.txt
