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
    echo "=== Test 1: get version and features from server ==="
    matrix-commander --rest GET "" "__homeserver__/_matrix/client/versions"
    res=$?
    if [ "$res" == "0" ]; then
        echo "SUCCESS"
    else
        echo "FAILURE"
        let failures++
    fi
}

function test2() {
    echo "=== Test 2: send an unencrypted text message ==="
    # see https://matrix.org/docs/api/#put-/_matrix/client/v3/rooms/-roomId-/send/-eventType-/-txnId-
    matrix-commander --rest POST '{"msgtype":"m.text", "body":"hello"}' \
        "__homeserver__/_matrix/client/r0/rooms/__room_id__/send/\
m.room.message?access_token=__access_token__"
    res=$?
    if [ "$res" == "0" ]; then
        echo "SUCCESS"
    else
        echo "FAILURE"
        let failures++
    fi
}

function test3() {
    echo "=== Test 3: invoke 2 REST API calls at once, more efficient ==="
    ARGS=(
        "--rest"
        # first triple of args for 1st REST call
        "GET"
        ""
        "__homeserver__/_matrix/client/versions"
        # second triple of args for 2nd REST call
        "POST"
        '{"msgtype":"m.text", "body":"hello"}'
        "__homeserver__/_matrix/client/r0/rooms/__room_id__/send/\
m.room.message?access_token=__access_token__"
        # --access-token add this option if needed
    )
    echo "Using these args:" "${ARGS[@]}"
    matrix-commander "${ARGS[@]}"
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
test3

echo "Finished test series with $failures failures."

exit $failures
