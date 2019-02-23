#!/bin/bash
set -eu

MOUNT="$1"

function check_corruption () {
    # https://superuser.com/questions/949066/input-output-errors-using-encfs-folder-inside-dropbox-folder/981417#981417
    ! find "$MOUNT" -type f -exec cat {} \; 2>&1 >/dev/null | grep error
}

function check_too_many_files () {
    # not very mobile friendly if there are too many...
    local count="$(find "$MOUNT" | wc -l)"
    if (( count < 1000 )); then
        return
    fi
    
    2>&1 echo "Too many files!"
    for d in "$MOUNT/"*; do
        2>&1 echo "$d: "
        2>&1 find "$d" | wc -l
    done
}

failed=0

check_corruption     || failed=1
check_too_many_files || failed=1

exit "$failed"
