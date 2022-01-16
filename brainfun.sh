#!/bin/sh
if [ ! -z $1 ] 
then 
    if [ ! -z $2 ] 
	then 
		python3.10 brainfun/brainfun.py $1 -o $2
	else
		python3.10 brainfun/brainfun.py $1
fi
else
    echo "Missing parameter: 'file'"
fi