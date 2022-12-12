#!/usr/bin/env bash

# Creates a file like this:
# <--usage>
# Print usage.
# <-h>, <--help>
# Print help.
# <--manual>
# Print manual.
# <-d>, <--debug>
# Print debug information.
# <--log-level> DEBUG|INFO|WARNING|ERROR|CRITICAL [DEBUG|INFO|WARNING|ERROR|CRITICAL]
# Set log level.
# <--verbose>
# Set verbosity.
# Always pairs of lines: header line, content line ...

PATH=".:matrix_commander/:$PATH"
old_width=$(stty size | cut -d' ' -f2-)
stty cols 1000
matrix-commander --manual | sed '1,/^options:/d' |
    sed 's/^  //g' | sed '/^-/ s/  [ ]*/  \n                      /g' |
    sed '/^You are running/,$d' |
    sed -e :a -e '$!N;s/\(^ .*\)\n [ ]*/\1 /;ta' -e 'P;D' |
    sed 's/^ [ ]*//g' | sed '/^$/d' | sed 's/\(.*\)Details::\(.*\)/\1/g' |
    sed 's/[ \t]*$//' |
    sed 's/\(^--[^ ]*\)\(.*\)/<\1>\2/g' |
    sed 's/\(^-[a-z0-9]\)\(.*\)/<\1>\2/g' |
    sed 's/\(^<-[^,]*\) \(--[^ ]+\)\(.*\)/\1<\2>\3/g' |
    sed 's/\(^<-.*\)\(--[^ ]*\)\(.*\)/\1<\2>\3/g' >help.help.pre.txt

stty cols $old_width
stty size
echo -n "Max width: "
wc -L help.help.pre.txt
