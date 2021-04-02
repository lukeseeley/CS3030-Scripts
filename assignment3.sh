#!/bin/bash

if [[ -n $1 ]]; then
  hashpaths=$(mktemp)
  find $1 -type f -name "*" | xargs sha256sum > $hashpaths
else
  echo "No file path was given as argument"
  exit 1
fi

#cat $hashpaths
hashcount=$(mktemp)
cat $hashpaths | cut -d" " -f1  | sort | uniq -c | sort -n -t" " -k1 > $hashcount

hashfilter=$(mktemp)
while read hashtxt; do
#  echo "hash count: $hashtxt"
  count=$(echo $hashtxt | cut -d" " -f1)
#  echo "Count: $count"
  if [[ $count -gt 1  ]]; then
#    echo "This hash has duplicates"
    echo $hashtxt | cut -d" " -f2 >> $hashfilter
  fi
done < $hashcount

#cat $hashfilter
filepaths=$(mktemp)
while read hsh; do
  grep $hashpaths -e"$hsh" | tr -s " " | cut -d" " -f2 > $filepaths
#  cat $filepaths
  files=$(cat $filepaths | wc -l)
  count=1
  echo "The following files are duplicates:"

  while read path; do
    echo "   $count. $path"
    count=$((count +1))
  done < $filepaths

  input=""
  until [[ ($input == "0") || ($input -gt 0 && $input -le $files) ]]; do
    echo -n "Choose a file to delete (Enter number between 1-$files, or 0 to skip): "
    read -u 1 input
  done

  if [[ input -gt 0 ]]; then
    file=$(cat $filepaths | head -n$input | tail -n1)
    echo "Deleting $file"
    rm $file
  fi

  echo ""
done < $hashfilter
