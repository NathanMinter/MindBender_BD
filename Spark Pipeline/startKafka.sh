zookeeper-server-start.sh -daemon mon /home/n/opt/kafka-2.3.1/config/zookeeper.properties
kafka-server-start.sh -daemon mon /home/n/opt/kafka-2.3.1/config/server1.properties
kafka-console-consumer.sh --consumer-property group.id=twitter --bootstrap-server localhost:9099 --topic tweets
