#!/bin/bash


cd /home/glog/Desktop/WW_Control/pdEffects
echo glog | sudo alsa force-reload
pd -audioindev 5,7,9,12 -inchannels 1,1,1,1 -audiooutdev 3 -outchannels 1 effectTry1.pd
