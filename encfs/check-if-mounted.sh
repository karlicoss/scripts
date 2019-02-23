#!/bin/bash
set -eu
DIR="$(dirname "$0")"
MOUNT="$1"

if mount | grep "$MOUNT"; then
    "$DIR/check.sh" "$MOUNT"
else
   >&2 echo "$MOUNT is not mounted..."
fi

