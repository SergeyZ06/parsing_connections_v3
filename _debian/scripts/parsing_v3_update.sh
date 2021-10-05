#!/bin/bash

# This script is to provide updating of the python script 'parsing_connections_v3'
PATH_120_211="SergeyZ06@192.168.120.211:/home/SergeyZ06/parsing_connections_v3"
PATH_TEMPORARY="/home/zsv/parsing_connections_v3_"
PATH_CURRENT="/home/zsv/parsing_connections_v3"
PATH_BACKUP="/home/zsv/parsing_connections_v3_$(date +%F_%R)"
PATH_LOG_FILE="/home/zsv/logs/log_parsing_connections_v3_$(date +%F)"

# Making a report into the log file
printf "==========================================================================\n" &>> $PATH_LOG_FILE
printf "$(date) - parsing_connections_v3 update initiated:\n" &>> $PATH_LOG_FILE
printf "==========================================================================\n" &>> $PATH_LOG_FILE

# Receiving new script from 192.168.120.211
scp -r $PATH_120_211 $PATH_TEMPORARY &>> $PATH_LOG_FILE
# Emprowering
chmod 755 -R $PATH_TEMPORARY &>> $PATH_LOG_FILE
# Backuping
mv $PATH_CURRENT $PATH_BACKUP &>> $PATH_LOG_FILE
# Enabling new script
mv $PATH_TEMPORARY $PATH_CURRENT &>> $PATH_LOG_FILE

printf "Backup file has been created at following path:\n" &>> $PATH_LOG_FILE
printf "\t$PATH_BACKUP\n" &>> $PATH_LOG_FILE
printf "==========================================================================\n" &>> $PATH_LOG_FILE
printf "\n" &>> $PATH_LOG_FILE
