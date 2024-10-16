#!/bin/bash
# -y SharedDb(0 false 1 true)
# -x Size Buffer Key 
# -r [0->CB_INC_NORMAL , 1->CB_P_INC, 2->CB_NON_INC_NORMAL, 3->CB_P_NON_INC, 4->TB_INC_NORMAL , 5->TB_P_INC, 6->TB_NONINC_NORMAL, 7->TB_P_NONINC]
# -l [N MemTable] 
# -k [n_keys] 
# -w [MemTable Size] 
# -s [Parallelism of each operator replica]
systemd-run --quiet --user --scope -p MemoryMax=8192M -p MemorySwapMax=128M ../wtest -y 0 -x 16 -r 0 -l 1 -w 256 -s 1 -k 500000 &>"0_500000_1_out.txt" &
pid="$!";
pmap -x "$pid" | tail -1 > '0_500000_1_mem.txt';
while sleep 1;
do
if ps -p "$pid" &>/dev/null;
then
pmap -x "$pid" | tail -1 >> '0_500000_1_mem.txt';
else
mv metric_latency.json '0_500000_1_latency.txt';
break
fi
done
systemd-run --quiet --user --scope -p MemoryMax=8192M -p MemorySwapMax=128M ../wtest -y 0 -x 16 -r 0 -l 1 -w 256 -s 1 -k 500000 &>"1_500000_1_out.txt" &
pid="$!";
pmap -x "$pid" | tail -1 >'1_500000_1_mem.txt';
while sleep 1;
do
if ps -p "$pid" &>/dev/null;
then
pmap -x "$pid" | tail -1 >> '1_500000_1_mem.txt';
else
mv metric_latency.json '1_500000_1_latency.txt';
break
fi
done
systemd-run --quiet --user --scope -p MemoryMax=8192M -p MemorySwapMax=128M ../wtest -y 0 -x 16 -r 0 -l 1 -w 256 -s 1 -k 500000 &>"2_500000_1_out.txt" &
pid="$!";
pmap -x "$pid" | tail -1 >'2_500000_1_mem.txt';
while sleep 1;
do
if ps -p "$pid" &>/dev/null;
then
pmap -x "$pid" | tail -1 >> '2_500000_1_mem.txt';
else
mv metric_latency.json '2_500000_1_latency.txt';
break
fi
done
systemd-run --quiet --user --scope -p MemoryMax=8192M -p MemorySwapMax=128M ../wtest -y 0 -x 16 -r 0 -l 1 -w 256 -s 1 -k 500000 &>"3_500000_1_out.txt" &
pid="$!";
pmap -x "$pid" | tail -1 >'3_500000_1_mem.txt';
while sleep 1;
do
if ps -p "$pid" &>/dev/null;
then
pmap -x "$pid" | tail -1 >> '3_500000_1_mem.txt';
else
mv metric_latency.json '3_500000_1_latency.txt';
break
fi
done
systemd-run --quiet --user --scope -p MemoryMax=8192M -p MemorySwapMax=128M ../wtest -y 0 -x 16 -r 0 -l 1 -w 256 -s 1 -k 500000 &>"4_500000_1_out.txt" &
pid="$!";
pmap -x "$pid" | tail -1 >'4_500000_1_mem.txt';
while sleep 1;
do
if ps -p "$pid" &>/dev/null;
then
pmap -x "$pid" | tail -1 >> '4_500000_1_mem.txt';
else
mv metric_latency.json '4_500000_1_latency.txt';
break
fi
done