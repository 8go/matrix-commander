#!/bin/bash

# One may set similar values in the terminal before calling the script.
# export MC_EVENT="\$...some.long.event.id.starting.with.$"
# export MC_OPTIONS="-d --room \!...some.room.id:matrix.example.org "

# Pasted from the MSC.
# 3 example JSON event templates; %s will be replaced by printf.
JSON_EDIT_MSC2676='{ "type": "m.room.message", "content": { "body": "%s", "msgtype": "m.text", "m.new_content": { "body": "%s", "msgtype": "m.text" }, "m.relates_to": { "rel_type": "m.replace", "event_id": "%s" } } }'
JSON_REACT_MSC2677='{ "type": "m.reaction", "content": { "m.relates_to":
    { "rel_type": "m.annotation", "event_id": "%s", "key": "%s" } } }'
JSON_REPLY_AS_THREAD_MSC3440='{ "type": "m.room.message", "content": { "body": "%s", "msgtype": "m.text", "m.relates_to": { "rel_type": "m.thread", "event_id": "%s" } } }'

# getting some value to fill the templates
if [ "$MC_EVENT" != "" ]; then
    echo "Exellent. Variable MC_EVENT already set. Using \"$MC_EVENT\" as event id for testing."
else
    read -r -p "Provide a valid event id (or set environment variable MC_EVENT): " MC_EVENT
    echo "OK. Using \"$MC_EVENT\" as event id for testing."
fi
if [ "$MC_OPTIONS" != "" ]; then
    echo "Exellent. Variable MC_OPTIONS already set. Using \"$MC_OPTIONS\" as additional options for testing."
else
    echo "Optionally, set variable \"MC_OPTIONS\" for further options."
fi
TARGET_EVENT="$MC_EVENT"

# These 4 test cases should pass
printf "$JSON_EDIT_MSC2676" "Fallback body $(date +%H:%M:%S)" "Non-fallback body $(date +%H:%M:%S)" "$TARGET_EVENT" |
    matrix-commander.py --event - $MC_OPTIONS
# https://unicode.org/emoji/charts/full-emoji-list.html
# emoji: thumbs up: "👍"; heart: "♥"; smiley: "😀"
printf "$JSON_REACT_MSC2677" "$TARGET_EVENT" "😀" |
    matrix-commander.py --event - $MC_OPTIONS
printf "$JSON_REPLY_AS_THREAD_MSC3440" "Thread reply $(date +%H:%M:%S)" "$TARGET_EVENT" |
    matrix-commander.py --event - $MC_OPTIONS

printf "$JSON_EDIT_MSC2676" "Fallback body $(date +%H:%M:%S)" "Non-fallback body $(date +%H:%M:%S)" "$TARGET_EVENT" >event1.json
printf "$JSON_REACT_MSC2677" "$TARGET_EVENT" "👍" >event2.json
printf "$JSON_REPLY_AS_THREAD_MSC3440" "Thread reply $(date +%H:%M:%S)" "$TARGET_EVENT" >event3.json
echo "##############################################################"
echo "##############################################################"
echo "##############################################################"
matrix-commander.py --event event1.json event2.json event3.json -m "" $MC_OPTIONS
rm event1.json event2.json event3.json

echo "##############################################################"
echo "##############################################################"
echo "##############################################################"
#

# These 4 test cases should ***FAIL***. ***INCORRECT*** JSON objects.
BAD_JSON_EDIT_MSC2676='{ "type": "m.room.message", "fail-content": { "body": "%s", "msgtype": "m.text", "m.new_content": { "body": "%s", "msgtype": "m.text" }, "m.relates_to": { "rel_type": "m.replace", "event_id": "%s" } } }'
BAD_JSON_REACT_MSC2677='{ "type": "m.reaction-wrong", "content": { "m.relates_to": { "rel_type": "m.annotation", "event_id": "%s", "key": "%s" } } }'
BAD_JSON_REPLY_AS_THREAD_MSC3440='{ "missing-type": "m.room.message", "content": { "body": "%s", "msgtype": "m.text", "m.relates_to": { "rel_type": "m.thread", "event_id": "%s" } } }'
BAD_JSON_REACT_MSC2677_2='{ type": "m.reaction-wrong", "content": { "m.relates_to": { "rel_type": "m.annotation", "event_id": "%s", "key": "%s" } } }'
# These 4 test cases should ***FAIL***
# this will fail due to JSON not being MSC compliant
printf "$BAD_JSON_EDIT_MSC2676" "Fallback body $(date +%H:%M:%S)" "Non-fallback body $(date +%H:%M:%S)" "$TARGET_EVENT" |
    ./matrix-commander.py --event - $MC_OPTIONS
# This message will be ignored on server side because type is incorrect.
printf "$BAD_JSON_REACT_MSC2677" "$TARGET_EVENT" "♥" |
    ./matrix-commander.py --event - $MC_OPTIONS
# this will fail due to JSON not being MSC compliant
printf "$BAD_JSON_REPLY_AS_THREAD_MSC3440" "Thread reply $(date +%H:%M:%S)" "$TARGET_EVENT" |
    ./matrix-commander.py --event - $MC_OPTIONS
# this will fail due to not being valid JSON
printf "$BAD_JSON_REACT_MSC2677_2" "$TARGET_EVENT" "♥" |
    ./matrix-commander.py --event - $MC_OPTIONS
