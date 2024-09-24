#!/bin/bash

echo "turning off NTP"
timedatectl set-ntp no
echo "setting time to $1"
timedatectl set-time "$1"
echo "turning on NTP"
timedatectl set-ntp yes
