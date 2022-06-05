#!/bin/bash

# just in case PATH is not set correctly
PATH=".:./matrix_commander:../matrix_commander:$PATH"

function test1() {
    echo "=== Test 1: uploading and downloading a text file without encryption ==="
    TMPFILE="test.txt.tmp"
    mxc_key=$(matrix-commander --upload tests/test.txt --plain)
    echo "$mxc_key"         # has the URI, like "mxc://...   None"
    mxc="${mxc_key%    *}"  # before "    "
    key="${mxc_key##*    }" # after "    "
    echo "mxc is \"$mxc\""
    echo "key is \"$key\"" # None in our case, because plain-text
    rm -f "$TMPFILE"
    # download knows it is plain because we do not specify a key dictionary
    matrix-commander --download "$mxc" --file-name "$TMPFILE"
    diff "$TMPFILE" "tests/test.txt"
    res="$?"
    if [ "$res" == "0" ]; then
        echo "SUCCESS"
        echo "Let's look at the text."
        cat "$TMPFILE" # look at the text file
    else
        echo "FAILURE"
    fi
}

function test2() {
    echo "=== Test 2: uploading and downloading an image file with encryption ==="
    mxc_key=$(matrix-commander --upload tests/test.s.png)
    echo "$mxc_key"         # has the URI, like "mxc://...   {some key dictionary}"
    mxc="${mxc_key%    *}"  # before "    "
    key="${mxc_key##*    }" # after "    "
    echo "mxc is \"$mxc\""
    echo "key is \"$key\""
    rm -f "$TMPFILE"
    # download knows it is encrypted because we specify a key dictionary
    matrix-commander --download "$mxc" --file-name "$TMPFILE" --key-dict "$key"
    diff "$TMPFILE" "tests/test.s.png"
    res="$?"
    if [ "$res" == "0" ]; then
        echo "SUCCESS"
        type eog >/dev/null 2>&1 && {
            echo "Let's look at the image."
            eog "$TMPFILE" >/dev/null 2>&1
        }
    else
        echo "FAILURE"
    fi
    rm -f "$TMPFILE"
}

function test3() {
    echo "=== Test 3: uploading and downloading 2 text files without encryption ==="
    N=2 # 2 files to test
    TESTFILES=("tests/test.1.txt" "tests/test.2.txt")
    TMPFILES=("test.1.txt.tmp" "test.2.txt.tmp")
    rm -f "${TMPFILES[@]}"
    mxc_keys=$(matrix-commander --upload ${TESTFILES[0]} ${TESTFILES[1]} --plain)
    echo "$mxc_keys" # has the N URIs, like "mxc://...   None"
    MXCS=()
    KEYS=()
    for ii in $(seq $N); do
        echo "Handling file $ii"
        mxc_key=$(echo "$mxc_keys" | head -n $ii | tail -n 1)
        mxc="${mxc_key%    *}"  # before "    "
        key="${mxc_key##*    }" # after "    "
        echo "mxc is \"$mxc\""
        echo "key is \"$key\"" # None in our case, because plain-text
        MXCS+=("$mxc")         # append mxc to array
        KEYS+=("$key")         # append mxc to array
    done
    rm -f "${TMPFILES[0]}" "${TMPFILES[1]}"
    # download knows it is plain because we do not specify a key dictionary
    matrix-commander --download "${MXCS[0]}" "${MXCS[1]}" \
        --file-name "${TMPFILES[0]}" "${TMPFILES[1]}"
    for ii in $(seq $N); do
        ((ii = ii - 1))
        diff "${TMPFILES[$ii]}" "${TESTFILES[$ii]}"
        res="$?"
        if [ "$res" == "0" ]; then
            echo "SUCCESS"
            echo "Let's look at the text."
            cat "${TMPFILES[$ii]}" # look at the text file
        else
            echo "FAILURE"
        fi
        rm "${TMPFILES[$ii]}"
    done
}

function test4() {
    echo "=== Test 4: convert MXC to HTTP URL ==="
    TMPFILE="test.txt.tmp"
    rm -f "$TMPFILE"
    mxc_http=$(matrix-commander --mxc-to-http "${MXCS[0]}")
    echo "$mxc_http"          # has the URI and the URL
    mxc="${mxc_http%    *}"   # before "    "
    http="${mxc_http##*    }" # after "    "
    echo "mxc is \"$mxc\""
    echo "mxc_http is \"$http\""
    wget -O "$TMPFILE" "$http"
    diff "$TMPFILE" "tests/test.1.txt"
    res="$?"
    if [ "$res" == "0" ]; then
        echo "SUCCESS"
        echo "Let's look at the image."
        cat "$TMPFILE" # look at the text file
    else
        echo "FAILURE"
    fi
    rm -f "$TMPFILE"

}

function test5() {
    echo "=== Test 5: uploading and downloading 2 text files with encryption ==="
    N=2 # 2 files to test
    TESTFILES=("tests/test.1.txt" "tests/test.2.txt")
    TMPFILES=("test.1.txt.tmp" "test.2.txt.tmp")
    rm -f "${TMPFILES[@]}"
    mxc_keys=$(matrix-commander --upload ${TESTFILES[0]} ${TESTFILES[1]})
    echo "$mxc_keys" # has the N URIs, like "mxc://...   None"
    MXCS=()
    KEYS=()
    for ii in $(seq $N); do
        echo "Handling file $ii"
        mxc_key=$(echo "$mxc_keys" | head -n $ii | tail -n 1)
        mxc="${mxc_key%    *}"  # before "    "
        key="${mxc_key##*    }" # after "    "
        echo "mxc is \"$mxc\""
        echo "key is \"$key\"" # a key dict
        MXCS+=("$mxc")         # append mxc to array
        KEYS+=("$key")         # append mxc to array
    done
    rm -f "${TMPFILES[0]}" "${TMPFILES[1]}"
    # download knows it is encrypted because we do specify a key dictionary
    matrix-commander --download "${MXCS[0]}" "${MXCS[1]}" \
        --file-name "${TMPFILES[0]}" "${TMPFILES[1]}" \
        --key-dict "${KEYS[0]}" "${KEYS[1]}"
    for ii in $(seq $N); do
        ((ii = ii - 1))
        diff "${TMPFILES[$ii]}" "${TESTFILES[$ii]}"
        res="$?"
        if [ "$res" == "0" ]; then
            echo "SUCCESS"
            echo "Let's look at the text."
            cat "${TMPFILES[$ii]}" # look at the text file
        else
            echo "FAILURE"
        fi
        rm "${TMPFILES[$ii]}"
    done
}

function test6() {
    echo "=== Test 6: deleting MXC resources from content repository ==="
    echo "Note: This will FAIL if you do not have server admin permissions!"
    matrix-commander --delete-mxc "${MXCS[0]}" "${MXCS[1]}"
}

test1
test2
test3
test4
test5
test6
