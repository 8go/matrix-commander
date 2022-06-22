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

type eog >/dev/null 2>&1 || {
    echo "The test works better if you install 'eog'."
}

type convert >/dev/null 2>&1 || {
    echo "The test works better if you install 'convert' from ImageMagick."
}

function test1() {
    echo "=== Test 1: getting its own avatar ==="
    TMPFILE="test.png.tmp"
    rm -f "$TMPFILE"
    N=1
    mxc_urls=$(matrix-commander --get-avatar $MC_OPTIONS)
    echo "$mxc_urls" # has the N URIs and URLs, like "mxc://...   https://..."
    for ii in $(seq $N); do
        echo "Handling avatar $ii"
        mxc_url=$(echo "$mxc_urls" | head -n $ii | tail -n 1)
        mxc="${mxc_url%    *}"  # before "    "
        url="${mxc_url##*    }" # after "    "
        echo "mxc is \"$mxc\""
        echo "url is \"$url\""
        wget "$url" -O "$TMPFILE"
        type eog >/dev/null 2>&1 && {
            echo "Let's look at the avatar."
            eog "$TMPFILE" >/dev/null 2>&1
        }
        rm -f "$TMPFILE"
    done
}

function test2() {
    echo "=== Test 2: getting the avatars of 2 users ==="
    user1=$(matrix-commander --whoami) # get some user_id
    user2=$user1                       # now we have 2 user ids
    TMPFILE="test.png.tmp"
    rm -f "$TMPFILE"
    N=2
    mxc_urls=$(matrix-commander --get-avatar "$user1" "$user2" $MC_OPTIONS)
    echo "$mxc_urls" # has the N URIs and URLs, like "mxc://...   https://..."
    for ii in $(seq $N); do
        echo "Handling avatar $ii"
        mxc_url=$(echo "$mxc_urls" | head -n $ii | tail -n 1)
        mxc="${mxc_url%    *}"  # before "    "
        url="${mxc_url##*    }" # after "    "
        echo "    mxc is \"$mxc\""
        echo "    url is \"$url\""
        wget "$url" -O "$TMPFILE"
        echo "    Downloaded the avatar to \"$TMPFILE\"."
        ls -l "$TMPFILE"
        type eog >/dev/null 2>&1 && {
            echo "    Let's look at the avatar."
            eog "$TMPFILE" >/dev/null 2>&1
        }
        rm -f "$TMPFILE"
    done
}

function test3() {
    echo "=== Test 3: get the avatar, convert it to black-and-white, ==="
    echo "=== set the avatar to the new black-and-white one, ==="
    echo "=== set the avatar back to the original one. ==="

    TMPFILE="test.png.tmp"
    TMPFILEBW="test.png.bw.tmp"
    rm -f "$TMPFILE" "$TMPFILEBW"
    N=1
    mxc_urls=$(matrix-commander --get-avatar $MC_OPTIONS)
    echo "$mxc_urls" # has the N URIs and URLs, like "mxc://...   https://..."
    for ii in $(seq $N); do
        echo "Handling avatar $ii"
        mxc_url=$(echo "$mxc_urls" | head -n $ii | tail -n 1)
        mxc="${mxc_url%    *}"  # before "    "
        url="${mxc_url##*    }" # after "    "
        echo "    mxc is \"$mxc\""
        echo "    url is \"$url\""
        wget "$url" -O "$TMPFILE"
        echo "    Downloaded the avatar to \"$TMPFILE\"."
        ls -l "$TMPFILE"
        type eog >/dev/null 2>&1 && {
            echo "    Let's look at the avatar."
            eog "$TMPFILE" >/dev/null 2>&1
        }
        convert "$TMPFILE" -colorspace Gray "$TMPFILEBW"
        type eog >/dev/null 2>&1 && {
            echo "    Let's look at the new black-and-white avatar."
            eog "$TMPFILEBW" >/dev/null 2>&1
        }
        # avatars must not be encrypted, use --plain
        mxc_key=$(matrix-commander --upload "$TMPFILEBW" --plain)
        mxcbw="${mxc_key%    *}" # before "    "
        echo "    Uploaded the new black-and-white avatar to URI \"$mxcbw\"."
        matrix-commander --set-avatar $mxcbw $MC_OPTIONS
        echo "    Setted the new avatar. Have a look at your client."
        read -t 30 -p "Like the new avatar?"
        matrix-commander --set-avatar $mxc $MC_OPTIONS
        echo "    Setted the avatar to as it was before. Have a look at your client."
        read -t 30 -p "Prefer the old avatar?"
        echo "" # add linebreak after timeout
        echo "    Done. We set it back to the original."
        rm -f "$TMPFILE" "$TMPFILEBW"
    done
}

function test4() {
    echo "=== Test 4: exporting keys to file ==="
    TMPFILE="test.keys.tmp"
    matrix-commander --export-keys "$TMPFILE" "bad-passphrase-3582" $MC_OPTIONS
    echo "Here is the file with the exported keys:"
    ls -l "$TMPFILE"
}

function test5() {
    echo "=== Test 5: importing keys from file ==="
    TMPFILEBK="test.keys.bad.tmp"
    echo "bad key file" >"$TMPFILEBK"
    echo "This should fail because of bad keys file."
    matrix-commander --import-keys "$TMPFILEBK" "bad-passphrase-3582" $MC_OPTIONS
    echo "This should fail because of wrong passphrase."
    matrix-commander --import-keys "$TMPFILE" "wrong-passphrase" $MC_OPTIONS
    echo "This should work."
    # slow, many keys usually
    matrix-commander --import-keys "$TMPFILE" "bad-passphrase-3582" $MC_OPTIONS
    rm -f "$TMPFILE" "$TMPFILEBK"
}

function test6() {
    echo "=== Test 6: getting its own user profile ==="
    N=1
    dispname_mxc_url_others=$(matrix-commander --get-profile $MC_OPTIONS)
    echo "$dispname_mxc_url_others" # lines with 4 pieces of information
    for ii in $(seq $N); do
        echo "Handling user profile $ii"
        dispname_mxc_url_other=$(echo "$dispname_mxc_url_others" | head -n $ii | tail -n 1)
        # shellcheck disable=SC2207
        out=($(grep -Eo '    |.+' <<<"$dispname_mxc_url_other")) # split by "    "
        dispname="${out[0]}"                                     # before first "    "
        mxc="${out[1]}"                                          # after first "    " and before 2nd "    "
        url="${out[2]}"
        other="${out[3]}"
        echo "    displayname is \"$dispname\""
        echo "    mxc is \"$mxc\""
        echo "    url is \"$url\""
        echo "    other info is \"$other\""
    done
}

function test7() {
    echo "=== Test 7: getting the user profiles of 2 users ==="
    user1=$(matrix-commander --whoami) # get some user_id
    user2=$user1                       # now we have 2 user ids
    N=2
    dispname_mxc_url_others=$(matrix-commander --get-profile "$user1" "$user2" $MC_OPTIONS)
    echo "$dispname_mxc_url_others" # lines with 4 pieces of information
    for ii in $(seq $N); do
        echo "Handling user profile $ii"
        dispname_mxc_url_other=$(echo "$dispname_mxc_url_others" | head -n $ii | tail -n 1)
        # dispname="$(sed -n "s/\(.*\)    \(mxc[^ ]*\)    \(http[^ ]*\)    \(.*\)/\1/p")"
        # shellcheck disable=SC2207
        out=($(grep -Eo '    |.+' <<<"$dispname_mxc_url_other")) # split by "    "
        dispname="${out[0]}"                                     # before first "    "
        mxc="${out[1]}"                                          # after first "    " and before 2nd "    "
        url="${out[2]}"
        other="${out[3]}"
        echo "    displayname is \"$dispname\""
        echo "    mxc is \"$mxc\""
        echo "    url is \"$url\""
        echo "    other info is \"$other\""
    done
}

function test8() {
    echo "=== Test 8: getting the state of default room ==="
    matrix-commander --room-get-state $MC_OPTIONS \
        2>/dev/null |                               # remove debug info
        grep -v -e "^Error" |                       # remove error lines
        sed -n "s/\(\[.*\]\)\(    \![^ ]*\)/\1/p" | # remove room id at EOL
        sed "s/'/\"/g" |                            # substitute all 's as ' is not valid in JSON
        jq                                          # beautify
}

function test9() {
    echo "=== Test 9: getting the visibility of default room ==="
    visi_room=$(matrix-commander --room-get-visibility $MC_OPTIONS)
    visibility="${visi_room%    *}" # before "    "
    roomid="${visi_room##*    }"    # after "    "
    echo "    Visibility of room \"$roomid\" is \"$visibility\"."
}

function test10() {
    echo "=== Test 10: adding an alias to the default room ==="
    matrix-commander --room-set-alias $MC_OPTIONS
    res="$?"
    if [ "$res" == "0" ]; then
        echo "FAILURE. The program should have failed, but didn't."
    else
        echo "SUCCESS. The program failed as expected."
    fi

}

function test11() {
    echo "=== Test 11: adding an alias to the default room ==="
    matrix-commander --room-set-alias a b c $MC_OPTIONS
    res="$?"
    if [ "$res" == "0" ]; then
        echo "FAILURE. The program should have failed, but didn't."
    else
        echo "SUCCESS. The program failed as expected."
    fi

}

function test12() {
    echo "=== Test 12: adding an alias to the default room ==="
    matrix-commander --room-set-alias " spaces not allowed" r "mustStartWith#" r "" r $MC_OPTIONS
    res="$?"
    if [ "$res" == "0" ]; then
        echo "FAILURE. The program should have failed, but didn't."
    else
        echo "SUCCESS. The program failed as expected."
    fi

}

function test13() {
    echo "=== Test 13: adding an alias to the default room ==="
    matrix-commander --room-set-alias "#Testing-room-A" $MC_OPTIONS
    res="$?"
    if [ "$res" == "0" ]; then
        echo "SUCCESS. Alias set."
    else
        echo "FAILURE. Alias not set."
    fi

}

function test14() {
    echo "=== Test 14: adding an alias to the default room ==="
    matrix-commander --room-set-alias "#Testing-room-B" $MC_OPTIONS
    res="$?"
    if [ "$res" == "0" ]; then
        echo "SUCCESS. Alias set."
    else
        echo "FAILURE. Alias not set."
    fi

}

test1
test2
test3
test4
test5
test6
test7
test8
test9
test10
test11
test12
test13
test14
