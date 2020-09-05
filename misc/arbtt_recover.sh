#!/bin/bash
set -eux

CAPTURE_LOG="$1"

cd "$(dirname "$CAPTURE_LOG")"

systemctl --user stop arbtt.service
arbtt-recover -i capture.log -o capture.log.recovered

mv capture.log capture.log.bak
mv capture.log.recovered capture.log

echo "TODO systenctl --user start arbtt"
