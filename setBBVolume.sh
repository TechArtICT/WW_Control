#!/bin/bash

# the following need keys from ssh-copy-id then vol: 3, 12, 18
activeTrees=(2 4 5 6 7 8 9 10 11 13 14 15 16 17 19 20 21 22 23 24 25 26)
# activeTrees=(2)
vol="60%"

for i in ${activeTrees[@]}; do
    echo "setting tree $i to volume $vol"
    # ssh-copy-id debian@10.42.0.$i
    ssh debian@10.42.0.$i "sed -i '3s/.*/amixer -c 1 -- sset Speaker $vol/' ~/bin/streamAudio.sh && amixer -c 1 -- sset Speaker $vol"
done


