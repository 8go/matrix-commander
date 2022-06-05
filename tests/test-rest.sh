#!/bin/bash

# just in case PATH is not set correctly
PATH=".:./matrix_commander:../matrix_commander:$PATH"

function test1() {
    echo "=== Test 1: get version and features from server ==="
    res=$(matrix-commander --rest GET "" "__homeserver__/_matrix/client/versions" 2>&1)
    echo $res
    if [ "$(echo "$res" | grep -ci error)" == "0" ]; then
        echo "SUCCESS"
    else
        echo "FAILURE"
    fi
}

function test2() {
    echo "=== Test 2: send an unencrypted text message ==="
    res=$(matrix-commander --rest POST '{"msgtype":"m.text", "body":"hello"}' \
        "__homeserver__/_matrix/client/r0/rooms/__room_id__/send/\
m.room.message?access_token=__access_token__" 2>&1)
    echo $res
    if [ "$(echo "$res" | grep -ci error)" == "0" ]; then
        echo "SUCCESS"
    else
        echo "FAILURE"
    fi
}

test1
test2
