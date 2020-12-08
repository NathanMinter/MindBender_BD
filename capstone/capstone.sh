#!/bin/bash
bash /home/n/opt/MindBender_BD/capstone/startKafka.sh &
ttab 'bash /home/n/opt/MindBender_BD/capstone/startHive.sh' &
ttab 'bash /home/n/opt/MindBender_BD/capstone/startSpark.sh' &
ttab 'bash /home/n/opt/MindBender_BD/capstone/startProducer.sh' &
