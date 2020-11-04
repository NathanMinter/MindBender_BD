#!/usr/bin/bash

output=$(hadoop version 2>&1)

if [[ $output == *"not found"* ]];
	then
		echo "Installing Hadoop."
        sudo wget http://archive.apache.org/dist/hadoop/common/hadoop-2.7.3/hadoop-2.7.3.tar.gz
        tar xzf hadoop-2.7.3.tar.gz
fi

echo "Hadoop installed."

date