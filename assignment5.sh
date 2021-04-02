#!/bin/bash

if ! [[ -n "$1" ]]; then
  echo "You must provide a source directory as the first option"
  exit 1
fi

if ! [[ -d "$1" ]]; then
  echo "$1 is not a valid source directory"
  exit 1
fi

if [[ -n "$2" ]]; then
  if ! [[ -d "$2" ]]; then
    mkdir $2
  fi
else
  echo "You must provide a destination directory as the second option"
  exit 1
fi

#Begin Processing MP3 files
filelist=$(mktemp)
find $1 -type f -name "*.mp3" > $filelist
declare -A frameData

cat $filelist | while IFS= read -r file; do
  #Begin processing header information
  a=$(hexdump -s 6 -n 1 -ve '1/1 "%.2x"' "./$file")
  a=$(( 16#$a ))
  a=$(( $a<<21 ))
  b=$(hexdump -s 7 -n 1 -ve '1/1 "%.2x"' "./$file")
  b=$(( 16#$b ))
  b=$(( $b<<14 ))
  c=$(hexdump -s 8 -n 1 -ve '1/1 "%.2x"' "./$file")
  c=$(( 16#$c ))
  c=$(( $c<<7 ))
  d=$(hexdump -s 9 -n 1 -ve '1/1 "%.2x"' "./$file")
  d=$(( 16#$d ))
  d=$(( $d<<0 ))
  headsize=$(( $a | $b | $c | $d ))
  offset=10 #This is the byte offset for the current frame header
  proccessed=0 #This is to count how many bytes have been processed for the loop
  unset frameData
  declare -A frameData

  #Begin processing frame headers
  while [[ $proccessed -lt $headsize ]]; do
    frameID=$(hexdump -s $offset -n 4 -ve '1/1 "%.2x"' "./$file" | sed -re 's/01fffe//' | sed -re 's/[00]*$//'  | xxd -r -p)
    if ! [[ -n $frameID ]]; then #If the rest is just padding, then just stop looping
      break
    fi
    offset=$(( $offset + 4 ))
    frameSize=$(hexdump -s $offset -n 4 -ve '1/1 "%.2x"' "./$file")
    frameSize=$(( 16#$frameSize ))
    offset=$(( $offset + 4 ))
    flags=$(hexdump -s $offset -n 2 -ve '1/1 "%.2x"' "./$file")
    offset=$(( $offset + 2 ))
    data=$(hexdump -s $offset -n $frameSize -ve '1/1 "%.2x"' "./$file" | sed -re 's/01fffe//' | sed -re 's/[00]*$//' | xxd -r -p)
    #data=$(hexdump -s $offset -n $frameSize -ve '1/2 "\\u%04x"' "./$file" | sed -e's/\\ufeff//g' | sed -e 's/\\u0000//g'); printf "$data"
    offset=$(( $offset + $frameSize ))
    proccessed=$(( $proccessed + 10 + $frameSize ))

    frameData[$frameID]=$data
#    echo "The frame ID is $frameID, the frameSize is $frameSize, the data is $data"
  done
#  exit 0
  #Now being sorting
  artist=$(echo ${frameData[TPE1]})
  title=$(echo ${frameData[TIT2]} | tr "[:upper:]" "[:lower:]")

  if [[ -n $artist && -n $title ]]; then
    path="$2/music/$artist/"
    mkdir -p "$path" && cp "./$file" "$path/$title.mp3"

  else
    path="$2/music/Various"
    if ! [[ -n $title ]]; then
      mkdir -p "$path" && cp "./$file" "$path"
    else
      mkdir -p "$path" && cp "./$file" "$path/$title.mp3"
    fi
  fi
done

#Begin Processing MP4 files
find $1 -type f -name "*.mp4" > $filelist

cat $filelist | while IFS= read -r file; do
  date=$(stat "./$file" | grep -e "Modify" | awk '{print $2 " " $3}' | xargs -0 date "+%Y-%b" -d)
  path="$2/vidoes/$date"
  mkdir -p "$path" && cp "./$file" "$path"
done

#Begin Processing JPG files
find $1 -type f -name "*.jpg" > $filelist

cat $filelist | while IFS= read -r file; do
  date=$(stat "./$file" | grep -e "Modify" | awk '{print $2 " " $3}' | xargs -0 date "+%Y-%b" -d)
  path="$2/photos/$date"
  mkdir -p "$path" && cp "./$file" "$path"
done
