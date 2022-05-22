#!/bin/bash

FN="matrix-commander.py"

if ! [ -f "$FN" ]; then
    FN="../$FN"
    if ! [ -f "$FN" ]; then
        echo -n "ERROR: $(basename -- "$FN") not found. "
        echo "Neither in local nor in parent directory."
        exit 1
    fi
fi

PREFIX="VERSION = "
REGEX="^${PREFIX}\"20[0-9][0-9]-[0-9][0-9]-[0-9][0-9].*\""

if ! [ -f "$FN" ]; then
    echo "ERROR: File \"$FN\" not found."
else
    COUNT=$(grep --count -e "$REGEX" $FN)
    if [ "$COUNT" == "1" ]; then
        # NEWVERSION="$PREFIX\"$(date +%Y-%m-%d-%H%M%S)\""
        NEWVERSION="$PREFIX\"$(date +%Y-%m-%d)\""
        sed -i "s/$REGEX/$NEWVERSION/" $FN
        RETURN=$?
        if [ "$RETURN" == "0" ]; then
            echo "SUCCESS: Modified file $FN by setting version to $NEWVERSION."
            exit 0
        else
            echo "ERROR: could not change version to $NEWVERSION in $FN."
        fi
    else
        echo "Error while searching for $REGEX"
        grep -e "$PREFIX" $FN
        if [ "$COUNT" == "1" ]; then
            echo "ERROR: Version not found, expected 1 occurance."
        else
            echo "ERROR: Version found $COUNT times, expected 1 occurance."
        fi
    fi
fi
exit 1
