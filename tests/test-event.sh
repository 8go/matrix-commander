#!/bin/bash

# One may set similar values in the terminal before calling the script.
# export MC_EVENT="\$...some.long.event.id.starting.with.$"
# export MC_OPTIONS="-d --room \!...some.room.id:matrix.example.org "

# getting some required values to fill the placeholders in the templates
if [ "$MC_EVENT" != "" ]; then
    echo "Exellent. Variable MC_EVENT already set. " \
        "Using \"$MC_EVENT\" as event id for testing."
else
    read -r -p "Provide a valid event id (or set variable MC_EVENT): " MC_EVENT
    echo "OK. Using \"$MC_EVENT\" as event id for testing."
fi
if [ "$MC_OPTIONS" != "" ]; then
    echo "Exellent. Variable MC_OPTIONS already set. " \
        "Using \"$MC_OPTIONS\" as additional options for testing."
else
    echo "Optionally, set variable \"MC_OPTIONS\" for further options."
fi
TARGET_EVENT="$MC_EVENT"

MSC2676_EDIT=$(cat event-templates/template-msc2676-edit.json)
MSC2677_REACT=$(cat event-templates/template-msc2677-react.json)
MSC3440_THREAD=$(cat event-templates/template-msc3440-thread.json)

echo -e "\n\n\nThe first 3 test cases should pass successfully.\n\n\n"
printf "$MSC2676_EDIT" "Fallback body $(date +%H:%M:%S)" \
    "Non-fallback body $(date +%H:%M:%S)" "$TARGET_EVENT" >event1.json
# https://unicode.org/emoji/charts/full-emoji-list.html
# https://unicode-table.com/en/emoji/
# emoji: thumbs up: "👍"; heart: "❤"; smiley: "😀",
printf "$MSC2677_REACT" "$TARGET_EVENT" "❤" >event2.json
printf "$MSC3440_THREAD" "Thread reply $(date +%H:%M:%S)" \
    "$TARGET_EVENT" >event3.json

matrix-commander.py --event event1.json event2.json -m "" $MC_OPTIONS
# also test the stdin pipe logic
cat event3.json | matrix-commander.py --event - $MC_OPTIONS

echo -e "\n\n\nThe next 4 test cases should ***FAIL*** due to " \
    "***INCORRECT*** JSON objects.\n\n\n"
# This is how NOT to do events and event templates.
BAD_MSC2676_EDIT='{ "type": "m.room.message", "fail-content": { "body": "%s", "msgtype": "m.text", "m.new_content": { "body": "%s", "msgtype": "m.text" }, "m.relates_to": { "rel_type": "m.replace", "event_id": "%s" } } }'
BAD_MSC2677_REACT='{ "type": "m.reaction-wrong", "content": { "m.relates_to": { "rel_type": "m.annotation", "event_id": "%s", "key": "%s" } } }'
BAD_MSC3440_THREAD='{ "missing-type": "m.room.message", "content": { "body": "%s", "msgtype": "m.text", "m.relates_to": { "rel_type": "m.thread", "event_id": "%s" } } }'
BAD_MSC2677_REACT_2='{ type": "m.reaction-wrong", "content": { "m.relates_to": { "rel_type": "m.annotation", "event_id": "%s", "key": "%s" } } }'
# this will fail due to JSON not being MSC compliant
printf "$BAD_MSC2676_EDIT" "Fallback body $(date +%H:%M:%S)" \
    "Non-fallback body $(date +%H:%M:%S)" "$TARGET_EVENT" >event1.json
# This message will not fail, but it will be ignored on server side
# because type is incorrect.
printf "$BAD_MSC2677_REACT" "$TARGET_EVENT" "❤" >event2.json
# this will fail due to JSON not being MSC compliant
printf "$BAD_MSC3440_THREAD" "Thread reply $(date +%H:%M:%S)" \
    "$TARGET_EVENT" >event3.json
# this will fail due to not being valid JSON
printf "$BAD_MSC2677_REACT_2" "$TARGET_EVENT" "❤" >event4.json
# These 4 test cases should ***FAIL***
matrix-commander.py --event event1.json event2.json event3.json event4.json -m "" $MC_OPTIONS
rm event1.json event2.json event3.json event4.json # clean up
