#!/bin/bash

# Define the disk device
disk="/dev/sdb"

# Define the number of partitions
num_partitions=30

# Loop through each partition number
for ((i=1; i<=$num_partitions; i++)); do
    partition="${disk}${i}"
    mkfs.ext4 "$partition"
done