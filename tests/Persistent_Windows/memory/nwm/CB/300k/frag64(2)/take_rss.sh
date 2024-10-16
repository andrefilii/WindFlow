#!/bin/bash
for i in *mem.txt;
do
< "$i" tr -s " " | cut -d " " -f4 > "$i".dat;
done
