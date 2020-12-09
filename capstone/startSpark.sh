#!/bin/bash
spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.11:2.4.1,org.apache.spark:spark-streaming-kafka-0-8_2.11:2.3.2 ~/opt/MindBender_BD/capstone/consumer.py
