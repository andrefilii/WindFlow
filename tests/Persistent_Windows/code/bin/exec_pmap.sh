#!/bin/bash

# funzione chiamata in caso di sigint sullo script
CUR_PID=0
terminate() {
    if [[ $CUR_PID -ne 0 ]]; then
        echo "Terminazione script..."
        kill -SIGTERM $CUR_PID
    fi
    exit 1
}

# in caso di sigint chiama terminate()
trap terminate SIGINT

# vari slide su cui vengono effettuati i test (90% 50% 10% overlapping)
SLIDES=(3000000 15000000 27000000)

# cap di memoria (32GB): se viene superato il programma viene killato
MEM_CAP=32000000

for S in "${SLIDES[@]}"; do
    # file di log per salvare i pmap
    LOG_FILE_FULL="pmap_log_full_${S}.txt"
    LOG_FILE_TOT="pmap_log_tot_${S}.txt"
    OUTPUT_FILE="output_${S}.log"

    # esecuzione programma
    ./wtest -y 0 -x 32 -r 7 -l 1 -m 256 -p 3 -w 30000000 -s $S -k 1000 > $OUTPUT_FILE 2>&1 &
    PID=$!
    CUR_PID=$PID

    echo "Inizio monitoraggio del processo con PID $PID e slide $S"
    while ps -p $PID > /dev/null; do
        TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
        echo "############### [$TIMESTAMP] - {$PID} ###############" >> $LOG_FILE_FULL
        pmap -x $PID >> $LOG_FILE_FULL
        pmap -x $PID | grep "total kB" >> $LOG_FILE_TOT
        echo "###################################################################" >> $LOG_FILE_FULL
        echo "" >> $LOG_FILE_FULL

        TOTAL_MEM=$(pmap -x $PID | grep "total kB" | awk '{print $3}')
        if [[ $TOTAL_MEM -gt $MEM_CAP ]]; then
            echo "Cap di memoria superato ($TOTAL_MEM kB > $MEM_CAP kB)"
            kill -SIGTERM $PID
            break
        fi

        sleep 10
    done
    echo "Monitoraggio del processo con slide $S terminato"
done