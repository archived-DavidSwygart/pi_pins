#!/bin/bash
echo "git pull latest pi_pins code"
cd "$(dirname "$0")"
git pull
echo "pins/update.sh finished "
