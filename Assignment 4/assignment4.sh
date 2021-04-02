#!/bin/bash

if [[ -a "$1" ]]; then
  $logfile=$1
elif [[ -p /dev/stdin ]] || [[ ! -t 0 ]]; then
  $logfile=$(mktemp)
  while IFS= read -r line; do
    echo $line >> $logfile
  done
else
  echo "No input found on standard input"
  exit 1
fi

#First pass to filter data
passauth=$(mktemp)
cat $logfile | tr -s " " | grep -e "password" | grep -v "account" | grep -v "pam" > $passauth
unsortlog=$(mktemp)
cat passauthlog.txt | grep -v "invalid" | awk '{print $1 " " $2 " " $3 " " $9 " " $6 " " $11 " " $13}' | sed -e 's/Accepted/success/g' -e 's/Failed/fail/g' >> $unsortlog
cat passauthlog.txt | grep -e "invalid" | awk '{print $1 " " $2 " " $3 " " $11 " " $9 " " $13 " " $15}' >> $unsortlog

#Convert time to seconds for sorting
usSec=$(mktemp)
cat $unsortlog | while IFS= read -r line; do
  ufdate=$(echo $line | awk '{print $1 " " $2 " " $3}')
  date=$(date -d "$ufdate" "+%s")
  data=$(echo $line | awk '{print $4 " " $5 " " $6 " " $7}')
  echo "$date $data" >> $usSec
done

#Sort by time then user
sortLog=$(mktemp)
cat uspassSec.txt | sort -t" " -n -k1 -k2 -s > $sortLog

count=0 #Used for counting repeated failures, multiple successes will not be counted together
lastUser="" #Used for determining if it is another failure
lastLine="" #Used to determine if the line has changed (Stores the last line to insert, if there was a failure)

echo '"Date","time","username","success/fail/invalid","number of attempts","IP address"' > passlog.csv
cat $sortLog | while IFS= read -r line; do
  user=$(echo $line | cut -d" " -f2)
  result=$(echo $line | cut -d" " -f3)
  sdate=$(echo $line | cut -d" " -f1)
  date=$(date -d "@$sdate" "+%m-%d")
  tim=$(date -d "@$sdate" "+%H:%M")
  ip=$(echo $line | cut -d" " -f4)

  if [[ $result == "success" ]]; then
    if [[ $user == $lastUser ]]; then
      count=$((count +1))
      echo "\"$date\",\"$tim\",\"$user\",\"$result\",$count,\"$ip\"" >> passlog.csv
    else
      if [[ -n $lastLine ]]; then
        echo $lastLine >> passlog.csv
      fi

      echo "\"$date\",\"$tim\",\"$user\",\"$result\",1,\"$ip\"" >> passlog.csv
    fi
    lastLine=""; count=0
  else
    if [[ $user == $lastUser ]]; then
      count=$((count +1))
      lastLine="\"$date\",\"$tim\",\"$user\",\"$result\",$count,\"$ip\""
    else
      if [[ -n $lastLine ]]; then
        echo $lastLine >> passlog.csv
      fi

      count=1
      lastLine="\"$date\",\"$tim\",\"$user\",\"$result\",$count,\"$ip\""
    fi
  fi

  lastUser=$user
done

if [[ -n $lastLine ]]; then
  echo $lastLine >> passlog.csv
fi
