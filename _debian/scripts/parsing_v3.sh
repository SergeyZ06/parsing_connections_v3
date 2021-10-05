#!/bin/bash

# This script is to run python script 'parsing_connections_v3'
PATH_SCRIPT="/home/zsv/parsing_connections_v3/main.py"
PATH_LOG_FILE="/home/zsv/logs/log_parsing_connections_v3_$(date +%F)"

# Making a report into the log file
printf "=================================================================\n" &>> $PATH_LOG_FILE
printf "$(date) - parsing_connections_v3 started:\n" &>> $PATH_LOG_FILE
printf "=================================================================\n" &>> $PATH_LOG_FILE
python3.7 $PATH_SCRIPT cron_parsing_connections_v3 &>> $PATH_LOG_FILE
printf "=================================================================\n" &>> $PATH_LOG_FILE
printf "\n" &>> $PATH_LOG_FILE
