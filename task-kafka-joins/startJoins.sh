#!/bin/bash
bash /home/n/opt/MindBender_BD/task-kafka-joins/startKafka.sh &
ttab 'kafka-console-consumer.sh --bootstrap-server localhost:9099 --topic LeftTopic' &
ttab 'kafka-console-consumer.sh --bootstrap-server localhost:9093 --topic RightTopic' &
ttab 'bash /home/n/opt/MindBender_BD/task-kafka-joins/startLeft.sh' &
ttab 'bash /home/n/opt/MindBender_BD/task-kafka-joins/startRight.sh' &
ttab 'scala /home/n/opt/MindBender_BD/task-kafka-joins/outer.scala'