#!/bin/bash

# funzione chiamata in caso di sigint sullo script
CUR_PID=0
terminate() {
    echo "Terminazione script..."
    if [[ $CUR_PID -ne 0 ]]; then
        kill -SIGTERM $CUR_PID
    fi
    exit 1
}

# in caso di sigint chiama terminate()
trap terminate SIGINT

# cap di memoria (32GB): se viene superato il programma viene killato
MEM_CAP=32000000

SLIDES=(3000000 15000000 27000000)
PARALLELISMS=(1 4 8)
BUFFER=(64 128)
KEYS=(1000 10000 50000)

for S in "${SLIDES[@]}"; do
    DIR_NAME="slide_${S}"
    DIR_TOT="${DIR_NAME}/tot_${S}"
    DIR_FULL="${DIR_NAME}/full_${S}"
    DIR_OUT="${DIR_NAME}/out_${S}"

    mkdir -p "$DIR_NAME"
    mkdir -p "${DIR_TOT}"
    mkdir -p "${DIR_FULL}"
    mkdir -p "${DIR_OUT}"

    for K in "${KEYS[@]}"; do
        for B in "${BUFFER[@]}"; do
            for P in "${PARALLELISMS[@]}"; do
                # file di log per salvare i pmap
                LOG_FILE_FULL="${DIR_FULL}/full_P${P}_B${B}_K${K}.txt"
                LOG_FILE_TOT="${DIR_TOT}/tot_P${P}_B${B}_K${K}.txt"
                OUTPUT_FILE="${DIR_OUT}/output_P${P}_B${B}_K${K}.log"

                # esecuzione programma
                ./wtest -y 0 -x $B -r 7 -l 1 -m 256 -p $P -w 30000000 -s $S -k $K > $OUTPUT_FILE 2>&1 &
                PID=$!
                CUR_PID=$PID

                echo "Inizio monitoraggio del processo con PID $PID, buffer $B, slide $S, parallelismo $P, n chiavi $K"
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
                echo "Fine monitoraggio del processo con PID $PID, buffer $B, slide $S, parallelismo $P, n chiavi $K"
            done
        done
    done
done
