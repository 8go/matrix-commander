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
    user2=user1                        # now we have 2 user ids
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
        echo "mxc is \"$mxc\""
        echo "url is \"$url\""
        wget "$url" -O "$TMPFILE"
        echo "Downloaded the avatar to \"$TMPFILE\"."
        ls -l "$TMPFILE"
        type eog >/dev/null 2>&1 && {
            echo "Let's look at the avatar."
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
        echo "mxc is \"$mxc\""
        echo "url is \"$url\""
        wget "$url" -O "$TMPFILE"
        echo "Downloaded the avatar to \"$TMPFILE\"."
        ls -l "$TMPFILE"
        type eog >/dev/null 2>&1 && {
            echo "Let's look at the avatar."
            eog "$TMPFILE" >/dev/null 2>&1
        }
        convert "$TMPFILE" -colorspace Gray "$TMPFILEBW"
        type eog >/dev/null 2>&1 && {
            echo "Let's look at the new black-and-white avatar."
            eog "$TMPFILEBW" >/dev/null 2>&1
        }
        # avatars must not be encrypted, use --plain
        mxc_key=$(matrix-commander --upload "$TMPFILEBW" --plain)
        mxcbw="${mxc_key%    *}" # before "    "
        echo "Uploaded the new black-and-white avatar to URI \"$mxcbw\"."
        matrix-commander --set-avatar $mxcbw $MC_OPTIONS
        echo "Setted the new avatar. Have a look at your client."
        read -t 30 -p "Like the new avatar?"
        matrix-commander --set-avatar $mxc $MC_OPTIONS
        echo "Setted the avatar to as it was before. Have a look at your client."
        read -t 30 -p "Prefer the old avatar?"
        echo "" # add linebreak after timeout
        echo "Done. We set it back to the original."
        rm -f "$TMPFILE" "$TMPFILEBW"
    done
}

test1
test2
test3
