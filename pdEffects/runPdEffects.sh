#!/bin/bash

amixer -c 2 -- sset Mic Capture 100%
cd /home/glog/Desktop/WW_Control/pdEffects
# echo glog | sudo -S alsa force-reload
# if [ "X$(aplay -l | grep "card 0" | grep USB)" == "X" ]; then
#     pd -audioindev 5,7,9,11 -inchannels 1,1,1,1 -audiooutdev 13 -outchannels 1 effectTry1.pd
# else
#    pd -audioindev 1,3,5,7 -inchannels 1,1,1,1 -audiooutdev 9 -outchannels 1 effectTry1.pd
#fi
 pd -audioindev 4 -inchannels 1 -audiooutdev 4 -outchannels 1 effectTry1.pd
