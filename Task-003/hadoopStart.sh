#!/usr/bin/bash

output=$(jps)

if [[ ( $output != *"ResourceManager"* ) || ( $output != *"NodeManager"* ) ]];
	then
		echo "Starting YARN."
		start-yarn.sh
	else
		echo "YARN running."
fi

if [[ ( $output != *"SecondaryNameNode"* ) || ( $output != *" NameNode"* ) || ( $output != *"DataNode"* ) ]];
	then
		echo "Starting DFS."
		start-yarn.sh
	else
		echo "DFS running."
fi

echo "Hadoop running."

date

