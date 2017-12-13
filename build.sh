#!/bin/bash

set -x
TIME=$(/bin/date "+%Y%m%d-%H%M")
OUTPATH=$1

/bin/mount -t cifs -o username=poweruser,password=geminipower //172.16.200.50:${OUTPATH} /opt/server/
/bin/tar --exclude='build.sh' --exclude='.*' -czvf /opt/server/gemini-solution-builder-${TIME}.tar.gz gemini_solution_builder
/bin/umount /opt/server
