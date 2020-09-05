#!/bin/sh
set -u
# set -x

show_error () {
   # TODO shit. termux-notification shows me '$1 is unbound for some reason; whereas toast seems to work. ugh!'
   LD_LIBRARY_PATH=/data/data/com.termux/files/usr/lib /data/data/com.termux/files/usr/bin/termux-toast -b red -g bottom "$@"
# /data/data/com.termux/files/usr/bin/bash 
   #notify-send "$@"
  
   title="$1"
   content="$2"

   /data/data/com.termux/files/usr/bin/termux-notification -t "error! $1" -c "$2"
}


output=$(2>&1 "$@")
rc="$?"

# todo not sure about this..
echo "$output"

if [ $rc -ne 0 ]; then
# TODO collect logs??
   show_error "$* exited with code $rc" "$output"
fi
