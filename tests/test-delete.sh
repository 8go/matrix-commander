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

function test1() {
    echo "=== Test 1: send a message, get event id, delete msg ==="
    echo "Watch it in your client, e.g. Element. Messge arrives, message is removed."
    respd=$(matrix-commander -m "Want to get event id for this message." $MC_OPTIONS 2>&1)
    resp=$(echo "$respd" | grep "INFO: ")
    room_id=$(echo $resp | awk -F'"' '{print $4}')
    event_id=$(echo $resp | awk -F'"' '{print $6}')
    echo "room: $room_id"
    echo "event: $event_id"
    matrix-commander --room-delete-content "$room_id" "$event_id" "Just testing."
}

function test2() {
    echo "=== Test 2: send a message, get event id, delete msg ==="
    echo "Watch it in your client, e.g. Element. Messge arrives, message is removed."
    ev_rm_msg=$(matrix-commander -m "Want to get event id for this message too." --print-event-id $MC_OPTIONS 2>/dev/null)
    echo "stdout was: $ev_rm_msg"
    # shellcheck disable=SC2207
    out=($(grep -Eo '    |.+' <<<"$ev_rm_msg")) # split by "    "
    event_id="${out[0]}"                        # before first "    "
    room_id="${out[1]}"                         # after first "    " and before 2nd "    "
    echo "room: $room_id"
    echo "event: $event_id"
    matrix-commander --room-delete-content "$room_id" "$event_id" "Just testing this."
}

test1
test2
