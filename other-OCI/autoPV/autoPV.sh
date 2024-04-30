#!/bin/bash

# Define the base YAML template for a PV
pv_template='
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-storage-%d
spec:
  capacity:
    storage: 75Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: local-storage
  local:
    path: /mnt/partition%d
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: local-storage
          operator: In
          values:
          - "yes"
'

# Loop to generate 30 PV YAML files
for i in {1..30}; do
  printf "$pv_template" "$i" "$i" > pv-"$i".yaml
done




#lets go ahead execute the yamls
# Get the directory of the script
script_dir=$(dirname "$0")

# Loop to apply each YAML file
for file in "$script_dir"/*.yaml; do
    oc apply -f "$file"
done