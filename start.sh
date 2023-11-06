#!/bin/bash
#separate numbers in array with spaces, not commas:
# activeTrees=(2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26)
activeTrees=(15)
numTrees=${#activeTrees[@]}
pythonDir="/home/ww/projects/whispering/mainControl"
test="false"
testPdSend="false"
jsonFile="allTheModes.json"

if [ "X$1" == "X" ]; then
    mode=All
else
    mode=$1
fi

# start jack if not already running
if [ "$(ps aux | grep jackd | wc -l)" == "1" ]; then
    if [ "$test" == "true" ]; then
        nohup /usr/bin/jackd -v -dalsa -dhw:Generic_1 -r48000 -S >/dev/null 2>&1 &
    else
        nohup /usr/bin/jackd -v -d dummy -r11025 >/dev/null 2>&1 &
    fi
fi

# don't go on unless jack started
while [ "$(jack_lsp 2>&1 | grep "server is not running or" | wc -l)" == "1" ]; do
    echo "waiting for jack to start"
    sleep 1
done
echo "Jack started"

#get to Pd directory
cd $pythonDir
# cd ..

# start master Pd control
pd masterVolume.pd &
# start Pd, Zita, and connect them
for i in ${activeTrees[@]}; do
    port=0$i
    port=${port: -2}
    zyport=40$port
    pyport=30$port
    ledport=60$port
    echo "ledport: $ledport"
    if [ "$(jack_lsp | grep puredata$i | wc -l)" == "0" ]; then
        if [ "$testPdSend" == "true" ]; then
            pd -jack -callback -jackname puredata$i -nojackconnect -inchannels 0 -outchannels 1 -send "pyPort $pyport" -send "port4LEDs $ledport" -send "port4LEDsTest $ledport" pdServers/playerServer.pd &
        else
            pd -jack -callback -jackname puredata$i -nojackconnect -inchannels 0 -outchannels 1 -send "pyPort $pyport" -send "port4LEDs $ledport" pdServers/playerServer.pd &
        fi
    fi
    if [ "$test" != "true" ]; then
        ./monitor.sh $i $zyport
    fi
done

# get to Python directory
cd $pythonDir

# start python main command central if it isn't already running:
if [ "$(ps aux | grep "python test.py" | wc -l)" == "1" ]; then
    source .venv/bin/activate
    python control.py $jsonFile -m $mode
fi
