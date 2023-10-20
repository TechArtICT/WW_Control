#!/bin/bash
#separate numbers in array with spaces, not commas:
activeTrees=(3)
numTrees=${#activeTrees[@]}
pythonDir="/home/ww/projects/whispering/mainControl"
# start jack if not already running
if [ "`ps aux | grep jackd | wc -l`" == "1" ];
then
    nohup /usr/bin/jackd -v -d dummy -r11025 > /dev/null 2>&1 &
fi

# don't go on unless jack started
while [ "`jack_lsp 2>&1 | grep "server is not running or" | wc -l`" == "1" ];
do
        echo "waiting for jack to start"
        sleep 1
done
echo "Jack started"

#get to Pd directory
cd $pythonDir
cd ..

# start Pd, Zita, and connect them
for i in ${activeTrees[@]}; do
    port=0$i
    port=${port: -2}
    zyport=40$port
    pyport=30$port
    echo $port
    if [ "`jack_lsp | grep puredata$i | wc -l`" == "0" ];
    then
        pd -jack -callback -jackname puredata$i -nojackconnect -inchannels 0 -outchannels 1 -send "pyPort $pyport" pdServers/playerServer.pd &
    fi
    if [ "`jack_lsp | grep zita$i | wc -l`" == "0" ];
    then
        zita-j2n 10.42.0.$i $zyport --16bit --chan 1 --jname zita$i &
    fi
    while [ "`jack_lsp | grep puredata$i | wc -l`" == "0" ];
    do
        echo "waiting for Pd instance to come up"
        sleep 1
    done
    jack_connect puredata$i:output_1 zita$i:in_1
done

# get to Python directory
cd $pythonDir

# start python main command central if it isn't already running:
if [ "`ps aux | grep "python test.py" | wc -l`" == "1" ];
then
    source .venv/bin/activate
    python test.py
fi
