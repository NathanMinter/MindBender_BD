#!/bin/bash
zookeeper-server-start.sh -daemon /home/n/opt/kafka-2.3.1/config/zookeeper.properties
kafka-server-start.sh -daemon /home/n/opt/kafka-2.3.1/config/server1.properties
kafka-server-start.sh -daemon /home/n/opt/kafka-2.3.1/config/server2.properties
kafka-server-start.sh -daemon /home/n/opt/kafka-2.3.1/config/server3.properties
kafka-console-consumer.sh --bootstrap-server localhost:9099 --topic capstone
