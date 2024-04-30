#!/bin/bash

# Define the disk device
disk="/dev/sdb"

# using gdisk instead of fdisk bc we can make more partitions. this will create 30 partitions each 80 gb each which still leaves some space open.
{
  for i in {1..30}; do
    cat <<EOF
n


+80G

EOF
  done
  echo "w"
  echo "y"
} | sudo gdisk $disk