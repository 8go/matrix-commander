#!/bin/bash

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
    cat "$TMPFILE" # look at the image
else
    echo "FAILURE"
fi

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
