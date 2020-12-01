#!/bin/bash
zookeeper-server-start.sh -daemon /home/n/opt/kafka-2.3.1/config/zookeeper.properties
kafka-server-start.sh -daemon /home/n/opt/kafka-2.3.1/config/server1.properties
kafka-server-start.sh -daemon /home/n/opt/kafka-2.3.1/config/server2.properties
kafka-server-start.sh -daemon /home/n/opt/kafka-2.3.1/config/server3.properties
kafka-console-consumer.sh --bootstrap-server localhost:9099 --topic reddit &
ttab 'hive --service metastore' &
ttab 'spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.4 ~/opt/MindBender_BD/reddit-pipeline/reddit-consumer.scala' &
ttab 'python3 /home/n/opt/MindBender_BD/reddit-pipeline/reddit-producer.py' &
