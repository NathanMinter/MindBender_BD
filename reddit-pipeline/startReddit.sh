#!/bin/bash
bash /home/n/opt/MindBender_BD/reddit-pipeline/startKafka.sh &
ttab 'bash /home/n/opt/MindBender_BD/reddit-pipeline/startHive.sh' &
ttab 'bash /home/n/opt/MindBender_BD/reddit-pipeline/startSpark.sh' &
ttab 'bash /home/n/opt/MindBender_BD/reddit-pipeline/startProducer.sh' &
