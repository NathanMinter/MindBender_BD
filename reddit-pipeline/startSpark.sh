#!/bin/bash
spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.3.2 ~/opt/MindBender_BD/reddit-pipeline/reddit-consumer.py
