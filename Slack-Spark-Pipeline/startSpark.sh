#!/bin/bash
spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.4 ~/opt/MindBender_BD/Slack-Spark-Pipeline/consumer.py
