#!/bin/bash

generate_timestamped_filename() {
    timestamp=$(date +"%Y%m%d_%H%M%S")
    echo "../test_results/SOL4_output_${timestamp}.txt"
}

# parametri programma
program="../code/bin/wtest"
params="-y 0 -x 32 -r 7 -l 1 -m 256 -p 1 -w 30000000 -s 15000000 -k 150000"
memory_limits=("2G" "4G" "8G")
output_file=$(generate_timestamped_filename)
metric_file="metric_latencysdp.json"

# Pulisci il file latency.txt se esiste
> "$output_file"

for mem_limit in "${memory_limits[@]}"; do
    echo "--- Eseguo con un cap di memoria: $mem_limit ---"
    echo "--- Eseguo con un cap di memoria: $mem_limit ---" >> "$output_file"
    
    # eseguo il programma con cap di memoria
    systemd-run --user --scope -p MemoryMax=$mem_limit -p MemorySwapMax=128M $program $params | tee -a "$output_file"
    
    # controllo se è stato generato l'output
    if [[ -f "$metric_file" ]]; then
        # aggiungo in coda
        cat "$metric_file" >> "$output_file"
        
        echo -e "\n--- Fine esecuzione con MemoryMax=$mem_limit ---\n" >> "$output_file"

        rm $metric_file
    else
        echo -e "\nKILLED\n--- Fine esecuzione con MemoryMax=$mem_limit ---\n" >> "$output_file"
        echo "File $metric_file non trovato!"
    fi
done

echo "Script completato. Risultati salvati in $output_file."