#!/bin/bash
online=`echo TechArtICT | sudo -S arp-scan -l -I br2`
echo "The following trees/pods/whatevers are offline:"
for i in {2..26}; do
    	if [ "X$(echo $online | grep 0.$i[[:space:]])" == "X" ]; then
		echo "$i"
	fi
done
