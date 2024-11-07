import re
import matplotlib.pyplot as plt
from datetime import datetime

# Nome del file di log generato dallo script bash
log_file = 'pmap_log_tot.txt'

# Pattern per estrarre il totale kB e RSS dalla riga "total kB"
total_pattern = r"total kB\s+(\d+)\s+(\d+)"

# Liste per salvare i dati
timestamps = []
total_kb_values = []
rss_values = []

# Tempo iniziale (partenza da 0 secondi)
start_time = 10

# Legge il file di log e raccoglie i dati
with open(log_file, 'r') as file:
    for line in file:
        total_match = re.search(total_pattern, line)
        
        if total_match:
            # Estrai i valori della memoria totale e RSS
            total_kb = int(total_match.group(1))
            rss = int(total_match.group(2))

            # Aggiungi i valori alle liste
            total_kb_values.append(total_kb / 1024)
            rss_values.append(rss / 1024)
            timestamps.append(start_time)  # Aggiungi un timestamp fittizio (per visualizzazione)
            start_time += 10;

# Verifica se sono stati raccolti dati
if not timestamps or not total_kb_values or not rss_values:
    print("Nessun dato trovato nel file di log.")
    exit()

# Normalizzazione dell'asse Y per partire dal minimo rilevato
min_y = min(min(total_kb_values), min(rss_values))

timestamps_minutes = [t / 60 for t in timestamps]

# Crea il grafico
plt.figure(figsize=(12, 6))
plt.plot(timestamps_minutes, total_kb_values, label='Totale MB', marker='o', linestyle='-', color='r')
plt.plot(timestamps_minutes, rss_values, label='Memoria residente (RSS)', marker='o', linestyle='-', color='b')
plt.title("Andamento dell'utilizzo della memoria (totale e RSS)")
plt.xlabel("Tempo (minuti)")
plt.ylabel("Memoria (MB)")
plt.grid(True)
plt.xticks(rotation=45)
plt.legend()

# Imposta i limiti dell'asse Y per partire dal minimo rilevato
plt.ylim(min_y - (0.10 * min_y), max(max(total_kb_values), max(rss_values)) * 1.05)

plt.tight_layout()

# salva il grafico
plt.savefig('grafico_memoria_'+datetime.now().strftime("%Y%m%dT%H:%M:%S")+'.png', bbox_inches='tight')

