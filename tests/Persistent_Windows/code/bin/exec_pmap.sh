#!/bin/bash

SLIDES=(3000000 15000000 27000000 30000000 40000000)

for S in "${SLIDES[@]}"; do
    # file di log per salvare i pmap
    LOG_FILE_FULL="pmap_log_full_${S}.txt"
    LOG_FILE_TOT="pmap_log_tot_${S}.txt"
    OUTPUT_FILE="output_${S}.log"

    # esecuzione programma
    ./wtest -y 0 -x 32 -r 7 -l 1 -m 256 -p 1 -w 30000000 -s $S -k 150000 > $OUTPUT_FILE 2>&1 &
    PID=$!

    echo "Inizio monitoraggio del processo con PID $PID e slide $S"
    while ps -p $PID > /dev/null; do
        TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
        echo "############### [$TIMESTAMP] - {$PID} ###############" >> $LOG_FILE_FULL
        pmap -x $PID >> $LOG_FILE_FULL
        pmap -x $PID | grep "total kB" >> $LOG_FILE_TOT
        echo "###################################################################" >> $LOG_FILE_FULL
        echo "" >> $LOG_FILE_FULL
        sleep 10
    done
    echo "Monitoraggio del processo con slide $S terminato"
done