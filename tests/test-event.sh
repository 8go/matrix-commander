#!/bin/bash

# just in case PATH is not set correctly
PATH=".:./matrix_commander:../matrix_commander:$PATH"

# One may set similar values in the terminal before calling the script.
# export MC_OPTIONS="-d --room \!...some.room.id:matrix.example.org "

# getting some required values to fill the placeholders in the templates
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

MSC2676_EDIT=$(cat event-templates/template-msc2676-edit.json)
MSC2677_REACT=$(cat event-templates/template-msc2677-react.json)
MSC3440_THREAD=$(cat event-templates/template-msc3440-thread.json)

rm -f event1.json event2.json event3.json event4.json # clean up

echo "Sending msg to get new event id."
evid_rm_txt=$(matrix-commander -m "Hi" --print-event-id $MC_OPTIONS)
echo "Returned $evid_rm_txt"
if [[ "$evid_rm_txt" == "" ]]; then
    echo "FAILURE."
    let failures++
fi
out=($(grep -Eo '    |.+' <<<"$evid_rm_txt")) # split by "    "
evid="${out[0]}"                              # before first "    "
echo "Returned event id is $evid"
TARGET_EVENT="$evid"
echo "TARGET_EVENT id is $TARGET_EVENT"

echo -e "\n\n\nThe first 3 test cases should pass successfully.\n\n\n"
printf "$MSC2676_EDIT" "Fallback body $(date +%H:%M:%S)" \
    "Non-fallback body $(date +%H:%M:%S)" "$TARGET_EVENT" >event1.json
# https://unicode.org/emoji/charts/full-emoji-list.html
# https://unicode-table.com/en/emoji/
# emoji: thumbs up: "👍"; heart: "❤"; smiley: "😀",
printf "$MSC2677_REACT" "$TARGET_EVENT" "❤" >event2.json
printf "$MSC3440_THREAD" "Thread reply $(date +%H:%M:%S)" \
    "$TARGET_EVENT" >event3.json

matrix-commander --event event1.json event2.json $MC_OPTIONS
res=$?
if [ "$res" == "0" ]; then
    echo "SUCCESS"
else
    echo "FAILURE"
    let failures++
fi
# also test the stdin pipe logic
cat event3.json | matrix-commander --event - $MC_OPTIONS
res=$?
if [ "$res" == "0" ]; then
    echo "SUCCESS"
else
    echo "FAILURE"
    let failures++
fi

echo -e "\n\n\nThe next 4 test cases should ***FAIL*** due to" \
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
cat event2.json | matrix-commander --event event1.json - event3.json event4.json $MC_OPTIONS
res=$?
if [ "$res" == "0" ]; then
    echo "UNEXPECTED SUCCESS == FAILURE"
    let failures++
else
    echo "EXPECTED FAILURE == SUCCESS"
fi
rm event1.json event2.json event3.json event4.json # clean up

echo "Finished test series with $failures failures."

exit $failures
