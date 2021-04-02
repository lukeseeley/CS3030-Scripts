#!/bin/bash

if [[ $# -eq 1 && $1 == "--help" ]]; then
  echo "Usage  $0 [--help] [-w <name>]"
  echo "       --help Print this help message"
  echo "       -w <name> Print name three times"
  exit 1
fi

echo "This script can do 3 things:"
echo "  1. Check to see if hte user is the root user"
echo "  2. Check to see if the script is runing on Linux OS"
echo "  3. Check to see if the -w argument was given"
echo ""
echo -n "What would you like to do (1, 2, 3):"
read option

if [[ $option -eq 1 ]]; then
  if [[ $UID -eq 0 ]]; then
    echo "The current user is root"
  else
    echo "The current user is $UID"
  fi
elif [[ $option -eq 2 ]]; then
  os_name=$(uname -s)
  if [[ $os_name == "Linux" ]]; then
    echo "The script is currently running on Linux"
  else
    echo "The script is not running on linux, but is currently running on $os_name"
  fi
elif [[ $option -eq 3 ]]; then
  if [[ $1 == "-w" ]]; then
    if [[ -n $2 ]]; then
      echo "$2 $2 $2"
    else
      echo "Error: The second command line argument was not set"
    fi
  else
    echo "The -w argument was not given"
  fi
else
  echo "Invalid option given. You entered $option"
fi
