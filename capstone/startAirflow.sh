#!/usr/bin/bash
airflow webserver &&
ttab 'airflow scheduler'
