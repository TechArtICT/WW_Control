#!/bin/bash

# the following need keys from ssh-copy-id then vol: 18
# the following need restartIfJackIsJacked: 3, 18, 21
activeTrees=(2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 19 20 21 22 23 24 25 26)
# activeTrees=(3)
vol="60%"

for i in ${activeTrees[@]}; do
    	echo "setting vol $vol on tree $i:"
    	# ssh-copy-id debian@10.42.0.$i
    	ssh debian@10.42.0.$i "sed -i '3s/.*/amixer -c 1 -- sset Speaker $vol/' ~/bin/streamAudio.sh && amixer -c 1 -- sset Speaker $vol"
	# scp restartIfJackIsJacked.sh debian@10.42.0.$i:~/bin/.
	# ssh debian@10.42.0.$i "jack_lsp -c"
	# ssh debian@10.42.0.$i "chmod 755 ~/bin/restartIfJackIsJacked.sh"
	# ssh debian@10.42.0.$i "(crontab -l 2>/dev/null; echo '*/5 * * * * /home/debian/bin/restartIfJackIsJacked.sh') | crontab -"
done
