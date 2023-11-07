#!/bin/bash

i=$1
zyport=$2
oneShot=true
twoShot=true

while [ "$twoShot" = true ]; do
    if [ "$(jack_lsp | grep zita$i | wc -l)" == "0" ]; then
            zita-j2n 10.42.0.$i $zyport --16bit --chan 1 --jname zita$i &
    fi
    if [ "$oneShot" = true ]; then
        oneShot=false
        while [ "$(jack_lsp | grep puredata$i | wc -l)" == "0" ]; do
            echo "waiting for Pd instance to come up"
            sleep 1
        done
        jack_connect puredata$i:output_1 zita$i:in_1
    else
        if [ "$(jack_lsp | grep puredata$i | wc -l)" == "0" ]; then
            twoShot=false
        else
            jack_connect puredata$i:output_1 zita$i:in_1
        fi
    fi
    sleep 10
done