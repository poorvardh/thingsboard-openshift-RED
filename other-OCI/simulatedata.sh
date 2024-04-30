#!/bin/bash

# Loop x amount of times
for ((i=1; i<=20; i++))
do
    # generate random number
    temperature=$(( (RANDOM % 15) + 20 ))
    
    # random temperature value
    curl -v -X POST http://tb-node-thingsboard.apps.ostb.rei.local/api/v1/T1_TEST_TOKEN/telemetry --header "Content-Type:application/json" --data "{\"temperature\":$temperature}"
    #
    # need to add delay
    sleep 1
done

