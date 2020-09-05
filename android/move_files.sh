#!/bin/bash
# There is a bunch of directories in Android I'd like to cloud sync (via Syncthing in my case)
# - Android doesn't support symlinks
# - I couldn't get bind mounts to work (and they also require root)
# 
# The only two options left were
# - point Syncthing at each of the directories separately
#   However, this is repetitive, clutters the config and needs to be set up on each of the remote ends
# - move the files into directory, handled by Syncthing (/sdcard/syncthing)
#   This is what this script does

set -eu
function moveit {
    SRC="$1"
    TARGET="$2"
    
    [ -d "$SRC"    ] || { echo "$SRC   : NOT A DIR!"; exit 1; }
    [ -d "$TARGET" ] || { echo "$TARGET: NOT A DIR!"; exit 1; }
    
    # todo check if not empty first?
    # mv -v "$SRC/"* "$TARGET/"

    cd "$SRC"
    shopt -s globstar nullglob
    flist=(**/*)
    # ugh. otherwise if flist is empty, it fails below..
    if ! (( ${#flist[@]} )); then
       2>&1 echo "$SRC: nothing to move"
       return
    fi

    ## first, check that files aren't open (e.g. we might be recording a video)
    # hmm. bulk lsof seems to be faster...
    used=$(lsof "${flist[@]}" | wc -l)
    if (( $used != 0 )); then
        2>&1 echo "$SRC: SOME FILES ARE IN USE!!"
        2>&1 echo "${flist[@]}"
        exit 1
        # todo should be more defensive? propagate errors up somehow??
        # maybe move_files script should be called from the outside?
    fi
    ##

    for f in "${flist[@]}"; do
        # if modified less than three minutes ago, skip
        # this is so there is some time to share photo.. also sometimes things are cached in the gallery
        if (( $(date +%s) < $(date +%s -r "$f") + 3 * 60 )); then
            2>&1 echo "$SRC/$f: modified too recently, skipping for now"
            continue
        fi

        # todo not sure if mkdir + mv is easier??
        # todo keeps empty dirs.. but whatever
        rsync -a --no-recursive --progress --remove-source-files "$SRC/$f" "$TARGET/$f"
    done
}

# todo Music/Movies?
for d in "Download" "DCIM" "Pictures" "Talon" "VK/Downloads"; do
    moveit "/sdcard/$d" "/sdcard/syncthing/sdcard/$d"
done


# todo notify even on success or something?
