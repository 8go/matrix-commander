#!/bin/bash

# just in case PATH is not set correctly
PATH=".:./matrix_commander:../matrix_commander:$PATH"

# One may set similar values in the terminal before calling the script.
# export MC_OPTIONS="-d --room \!...some.room.id:matrix.example.org "

# getting some optional arguments
if [ "$MC_OPTIONS" != "" ]; then
    echo "Exellent. Variable MC_OPTIONS already set. " \
        "Using \"$MC_OPTIONS\" as additional options for testing."
else
    echo "Optionally, set variable \"MC_OPTIONS\" for further options."
fi

echo "Python version is: $(python --version)"
echo "GITHUB_WORKFLOW = $GITHUB_WORKFLOW"
echo "GITHUB_REPOSITORY = $GITHUB_REPOSITORY"
echo "MC_OPTIONS = $MC_OPTIONS"

if [[ "$GITHUB_WORKFLOW" != "" ]]; then # if in Github Action Workflow
    echo "I am in Github Action Workflow $GITHUB_WORKFLOW."
fi

failures=0

function test1() {
    echo "=== Test 1: get version in text format ==="
    matrix-commander --version
    res=$?
    if [ "$res" == "0" ]; then
        echo "SUCCESS"
    else
        echo "FAILURE"
        let failures++
    fi
}

function test2() {
    echo "=== Test 2: get version in JSON format ==="
    matrix-commander --version --output json
    res=$?
    if [ "$res" == "0" ]; then
        echo "SUCCESS"
    else
        echo "FAILURE"
        let failures++
    fi
}

test1
test2

echo "Finished test series with $failures failures."

exit $failures
