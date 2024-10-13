#!/bin/bash

systemd-run --user --scope -p MemoryMax=8192M -p MemorySwapMax=128M ./wtest -r 600 -w 30000000 -s 15000000 -k 500000 -n 1 -p true
#pid="$!";
#pmap -x "$pid" | tail -1 >'0_500000_1_mem.txt';
#while sleep 1;
#do
#if ps -p "$pid" &>/dev/null;
#then
#pmap -x "$pid" | tail -1 >> '0_500000_1_mem.txt';
#else
#mv metric_latency.json '0_500000_1_latency.txt';
#break
#fi
#done
#
#systemd-run --quiet --user --scope -p MemoryMax=4096M -p MemorySwapMax=128M ./wtest -r 60 -w 1000 -s 900 -k 500000 -n 1 &>"1_500000_1_out.txt" &
#pid="$!";
#pmap -x "$pid" | tail -1 >'1_500000_1_mem.txt';
#while sleep 1;
#do
#if ps -p "$pid" &>/dev/null;
#then
#pmap -x "$pid" | tail -1 >> '1_500000_1_mem.txt';
#else
#mv metric_latency.json '1_500000_1_latency.txt';
#break
#fi
#done
#
#systemd-run --quiet --user --scope -p MemoryMax=2048M -p MemorySwapMax=128M ./wtest -r 60 -w 1000 -s 900 -k 500000 -n 1 &>"2_500000_1_out.txt" &
#pid="$!";
#pmap -x "$pid" | tail -1 >'2_500000_1_mem.txt';
#while sleep 1;
#do
#if ps -p "$pid" &>/dev/null;
#then
#pmap -x "$pid" | tail -1 >> '2_500000_1_mem.txt';
#else
#mv metric_latency.json '2_500000_1_latency.txt';
#break
#fi
#done
#
#systemd-run --quiet --user --scope -p MemoryMax=1024M -p MemorySwapMax=128M ./wtest -r 60 -w 1000 -s 900 -k 500000 -n 1 &>"3_500000_1_out.txt" &
#pid="$!";
#pmap -x "$pid" | tail -1 >'3_500000_1_mem.txt';
#while sleep 1;
#do
#if ps -p "$pid" &>/dev/null;
#then
#pmap -x "$pid" | tail -1 >> '3_500000_1_mem.txt';
#else
#mv metric_latency.json '3_500000_1_latency.txt';
#break
#fi
#done