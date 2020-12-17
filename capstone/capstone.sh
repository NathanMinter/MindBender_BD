#!/bin/bash

output=$(jps)

if [[ $output != *"Kafka"* ]];
	then
		echo "Starting Kafka."
		bash /home/n/opt/MindBender_BD/capstone/startKafka.sh &
	else
		echo "Kafka running."
fi

if [[ $output != *"SparkSubmit"* ]];
	then
		echo "Starting Spark."
		ttab 'bash /home/n/opt/MindBender_BD/capstone/startSpark.sh' &
	else
		echo "Spark running."
fi

echo "Starting Producer."
ttab 'python3 /home/n/opt/MindBender_BD/capstone/latest.py' &
