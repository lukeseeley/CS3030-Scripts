#!/bin/bash

> sec.txt
if [[ $# -gt 0 && -n $1 ]]; then
  while read line; do
    date "+%s" -d "$line" 2>/dev/null  >> sec.txt
    if [[ $? -ne 0 ]]; then
      date "+%s" -d "@$line" >> sec.txt
    fi
  done < "$1"
elif [[ -p /dev/stdin ]] || [[ ! -t 0  ]] ; then 
  while read line; do
    date "+%s" -d "$line" 2>/dev/null  >> sec.txt
    if [[ $? -ne 0 ]]; then
      date "+%s" -d "@$line" >> sec.txt
    fi
  done
else
  echo "No input found" >&2
fi

sort sec.txt -n > sorted.txt

while read line; do
 date "+%d/%m/%Y" -d "@$line"
done < sorted.txt
