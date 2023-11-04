#!/bin/bash
process="jackd"

cpuUsage=$(top -bn2 -p $(pgrep $process) | grep $process | tail -n 1 | awk {'print $9;'} | cut -f1 -d'.')
# echo $cpuUsage
if [ "$cpuUsage" -gt "80" ]; then
        echo "temppwd" | sudo -S reboot
fi
