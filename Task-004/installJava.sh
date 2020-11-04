#!/usr/bin/bash

output=$(java -version 2>&1)

if [[ $output == *"not found"* ]];
	then
		echo "Installing Java."
        sudo apt install openjdk-8-jdk -y
fi

echo "Java installed."

date