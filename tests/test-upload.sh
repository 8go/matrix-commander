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

# in order to make it uniform and consistant between local execution
# and remote Github Action workflow, let's create the files on the fly
# even though we have test files locally.

MYDIR="" # "tests/"
if [[ "$MYDIR" != "" ]] && [[ "$MYDIR" != "." ]] && [[ "$MYDIR" != "./" ]]; then
    mkdir ${MYDIR}
fi
echo "test.txt" >${MYDIR}test.txt
echo "test.1.txt" >${MYDIR}test.1.txt
echo "test.2.txt" >${MYDIR}test.2.txt
echo '<?xml version="1.0" encoding="UTF-8" standalone="no"?><svg    width="2in"     height="2in"    viewBox="0 0 192 192"    version="1.1"    id="svg5"    inkscape:version="1.1.2 (0a00cf5339, 2022-02-04)"    sodipodi:docname="test2.svg"    xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"    xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"    xmlns="http://www.w3.org/2000/svg"    xmlns:svg="http://www.w3.org/2000/svg">   <sodipodi:namedview      id="namedview7"      pagecolor="#ffffff"      bordercolor="#666666"      borderopacity="1.0"      inkscape:pageshadow="2"      inkscape:pageopacity="0.0"      inkscape:pagecheckerboard="0"      inkscape:document-units="in"      showgrid="false"      inkscape:zoom="1.6234774"      inkscape:cx="26.486356"      inkscape:cy="95.166092"      inkscape:window-width="1471"      inkscape:window-height="1088"      inkscape:window-x="1486"      inkscape:window-y="346"      inkscape:window-maximized="1"      inkscape:current-layer="layer1" />   <defs      id="defs2" />   <g      inkscape:label="Layer 1"      inkscape:groupmode="layer"      id="layer1">     <rect        style="opacity:1;fill:#ff0000;stroke-width:100;stroke-linejoin:round"        id="rect868"        width="244.53682"        height="250.08047"        x="-25.254433"        y="-24.63847" />     <ellipse        style="opacity:1;fill:#0000ff;stroke-width:100;stroke-linejoin:round"        id="path1332"        cx="161.99794"        cy="215.58661"        rx="104.09753"        ry="91.778305" />   </g> </svg> ' >${MYDIR}test.s.svg
ls -l ${MYDIR}

function test1() {
    echo "=== Test 1: uploading and downloading a text file without encryption ==="
    TMPFILE="test.txt.tmp"
    mxc_key=$(matrix-commander --upload ${MYDIR}test.txt --plain)
    if [[ "$mxc_key" == "" ]]; then
        echo "FAILURE."
        let failures++
        return
    fi
    echo "$mxc_key"         # has the URI, like "mxc://...   None"
    mxc="${mxc_key%    *}"  # before "    "
    key="${mxc_key##*    }" # after "    "
    echo "mxc is \"$mxc\""
    echo "key is \"$key\"" # None in our case, because plain-text
    rm -f "$TMPFILE"
    # download knows it is plain because we do not specify a key dictionary
    matrix-commander --download "$mxc" --file-name "$TMPFILE"
    res="$?"
    if [ "$res" == "0" ]; then
        echo "SUCCESS."
    else
        echo "FAILURE."
        let failures++
    fi
    diff "$TMPFILE" "${MYDIR}test.txt"
    res="$?"
    if [ "$res" == "0" ]; then
        echo "SUCCESS"
        echo "Let's look at the text."
        cat "$TMPFILE" # look at the text file
    else
        echo "FAILURE"
        let failures++
    fi
}

function test2() {
    echo "=== Test 2: uploading and downloading an image file with encryption ==="
    mxc_key=$(matrix-commander --upload ${MYDIR}test.s.svg)
    if [[ "$mxc_key" == "" ]]; then
        echo "FAILURE."
        let failures++
        return
    fi
    # echo "$mxc_key"       # has the URI, like "mxc://...   {some key dictionary}"  # leaks keys
    mxc="${mxc_key%    *}"  # before "    "
    key="${mxc_key##*    }" # after "    "
    echo "mxc is \"$mxc\""
    echo "key is \"***\"" # "key is \"$key\"" hide for privacy, don't leak keys
    rm -f "$TMPFILE"
    # download knows it is encrypted because we specify a key dictionary
    matrix-commander --download "$mxc" --file-name "$TMPFILE" \
        --key-dict "$key"
    res="$?"
    if [ "$res" == "0" ]; then
        echo "SUCCESS."
    else
        echo "FAILURE."
        let failures++
    fi
    diff "$TMPFILE" "${MYDIR}test.s.svg"
    res="$?"
    if [ "$res" == "0" ]; then
        echo "SUCCESS"
        if [[ "$GITHUB_WORKFLOW" == "" ]]; then # skip in Github Action Workflow
            type eog >/dev/null 2>&1 && {
                echo "Let's look at the image."
                eog "$TMPFILE" >/dev/null 2>&1
            }
        fi
    else
        echo "FAILURE"
        let failures++
    fi
    rm -f "$TMPFILE"
}

function test3() {
    echo "=== Test 3: uploading and downloading 2 text files without encryption ==="
    N=2 # 2 files to test
    TESTFILES=("${MYDIR}test.1.txt" "${MYDIR}test.2.txt")
    TMPFILES=("test.1.txt.tmp" "test.2.txt.tmp")
    rm -f "${TMPFILES[@]}"
    mxc_keys=$(matrix-commander --upload ${TESTFILES[0]} ${TESTFILES[1]} --plain)
    if [[ "$mxc_keys" == "" ]]; then
        echo "FAILURE."
        let failures++
        return
    fi
    # echo "$mxc_keys" # has the N URIs, like "mxc://...   None"  # leaks keys
    MXCS=()
    KEYS=()
    for ii in $(seq $N); do
        echo "Handling file $ii"
        mxc_key=$(echo "$mxc_keys" | head -n $ii | tail -n 1)
        mxc="${mxc_key%    *}"  # before "    "
        key="${mxc_key##*    }" # after "    "
        echo "mxc is \"$mxc\""
        echo "key is \"***\"" # "key is \"$key\"" # None in our case, because plain-text  # leaks key
        MXCS+=("$mxc")        # append mxc to array
        KEYS+=("$key")        # append mxc to array
    done
    rm -f "${TMPFILES[0]}" "${TMPFILES[1]}"
    # download knows it is plain because we do not specify a key dictionary
    matrix-commander --download "${MXCS[0]}" "${MXCS[1]}" \
        --file-name "${TMPFILES[0]}" "${TMPFILES[1]}"
    res="$?"
    if [ "$res" == "0" ]; then
        echo "SUCCESS."
    else
        echo "FAILURE."
        let failures++
    fi
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
            let failures++
        fi
        rm "${TMPFILES[$ii]}"
    done
}

function test4() {
    echo "=== Test 4: convert MXC to HTTP URL ==="
    TMPFILE="test.txt.tmp"
    rm -f "$TMPFILE"
    mxc_http=$(matrix-commander --mxc-to-http "${MXCS[0]}")
    if [[ "$mxc_http" == "" ]]; then
        echo "FAILURE."
        let failures++
        return
    fi
    echo "$mxc_http"          # has the URI and the URL
    mxc="${mxc_http%    *}"   # before "    "
    http="${mxc_http##*    }" # after "    "
    echo "mxc is \"$mxc\""
    echo "mxc_http is \"$http\""
    wget -O "$TMPFILE" "$http"
    diff "$TMPFILE" "${MYDIR}test.1.txt"
    res="$?"
    if [ "$res" == "0" ]; then
        echo "SUCCESS"
        echo "Let's look at the text file."
        cat "$TMPFILE" # look at the text file
    else
        echo "FAILURE"
        let failures++
    fi
    rm -f "$TMPFILE"

}

function test5() {
    echo "=== Test 5: uploading and downloading 2 text files with encryption ==="
    N=2 # 2 files to test
    TESTFILES=("${MYDIR}test.1.txt" "${MYDIR}test.2.txt")
    TMPFILES=("test.1.txt.tmp" "test.2.txt.tmp")
    rm -f "${TMPFILES[@]}"
    mxc_keys=$(matrix-commander --upload ${TESTFILES[0]} ${TESTFILES[1]})
    if [[ "$mxc_keys" == "" ]]; then
        echo "FAILURE."
        let failures++
        return
    fi
    # echo "$mxc_keys" # has the N URIs, like "mxc://...   None"  # leaks keys
    MXCS=()
    KEYS=()
    for ii in $(seq $N); do
        echo "Handling file $ii"
        mxc_key=$(echo "$mxc_keys" | head -n $ii | tail -n 1)
        mxc="${mxc_key%    *}"  # before "    "
        key="${mxc_key##*    }" # after "    "
        echo "mxc is \"$mxc\""
        echo "key is \"***\"" # "key is \"$key\""# a key dict  # leaks keys
        MXCS+=("$mxc")        # append mxc to array
        KEYS+=("$key")        # append mxc to array
    done
    rm -f "${TMPFILES[0]}" "${TMPFILES[1]}"
    # download knows it is encrypted because we do specify a key dictionary
    matrix-commander --download "${MXCS[0]}" "${MXCS[1]}" \
        --file-name "${TMPFILES[0]}" "${TMPFILES[1]}" \
        --key-dict "${KEYS[0]}" "${KEYS[1]}"
    res="$?"
    if [ "$res" == "0" ]; then
        echo "SUCCESS."
    else
        echo "FAILURE."
        let failures++
    fi
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
            let failures++
        fi
        rm "${TMPFILES[$ii]}"
    done
}

function test6() {
    echo "=== Test 6: deleting MXC resources from content repository ==="
    echo "Note: This will FAIL if you do not have server admin permissions!"
    matrix-commander --delete-mxc "${MXCS[0]}" "${MXCS[1]}"
    res=$?
    if [ "$res" == "0" ]; then
        echo "SUCCESS"
    else
        echo "FAILURE, normal because server permissions are usually not available"
        # don't increment failures because this is expected
    fi
}

function test7() {
    echo "=== Test 7: deleting old resources from content repository ==="
    echo "Note: This will FAIL if you do not have server admin permissions!"
    matrix-commander --delete-mxc-before "20.01.2022 19:38:42" "1000000"
    res=$?
    if [ "$res" == "0" ]; then
        echo "SUCCESS"
    else
        echo "FAILURE, normal because server permissions are usually not available"
        # don't increment failures because this is expected
    fi
}

test1
test2
test3
test4
test5
test6
test7

rm -f ${MYDIR}test.txt
rm -f ${MYDIR}test.1.txt
rm -f ${MYDIR}test.2.txt
rm -f ${MYDIR}test.s.svg
if [[ "$MYDIR" != "" ]] && [[ "$MYDIR" != "." ]] && [[ "$MYDIR" != "./" ]]; then
    rmdir ${MYDIR}
fi

echo "Finished test series with $failures failures."

exit $failures
