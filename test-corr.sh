#!/usr/bin/env bash

# Customize these for your project:
COMMAND='java -jar ./CoulAdj.jar'
SAMPLES_DIR='./tests/samples/'
RESULTS_DIR='./tests/results/'
GOLDEN_DIR='./tests/'
# (Make sure the DIR variables end with a /backslash/ )

GOLDEN="${GOLDEN_DIR}golden.tsv"
evaluate_size(){
    local SAMPLE="${SAMPLES_DIR}sample-size-$1.png"
    local RESULT="${RESULTS_DIR}result-size-$1.tsv"
    $COMMAND "$SAMPLE" "$RESULT" &> /dev/null
    cmp --silent "$GOLDEN" "$RESULT" || echo "Size $1 failed"
}

evaluate_size 1
echo "Correctness test(s) finished"