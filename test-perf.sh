#!/usr/bin/env bash

# echo "This file is only here to demonstrate how to do a loop in bash."
#for ((i = 1 ; i <= 10 ; i++)); do
#    ./bitmap-colour-adjacencies "$SRC" "$DST" 2> /dev/null | tail -n1
#done

# Customize these for your project:
COMMAND='python ./CoulAdj-Py.py --profile'
SAMPLES_DIR='./tests/samples/'
RESULTS_DIR='./tests/results/'
GOLDEN_DIR='./tests/'
# (Make sure the DIR variables end with a /backslash/ )

# Usually, NB_LOOPS=10
NB_LOOPS=10

GOLDEN="${GOLDEN_DIR}golden.tsv"
evaluate_size(){
    local SAMPLE="${SAMPLES_DIR}sample-size-$1.png"
    local RESULT="${RESULTS_DIR}result-size-$1.tsv"
    for ((i = 1 ; i <= $NB_LOOPS ; i++)); do
        #echo -n "Size $1: "
        $COMMAND "$SAMPLE" "$RESULT"
    done
    cmp --silent "$GOLDEN" "$RESULT" || echo "Size $1 failed"
}

#evaluate_size 1
#evaluate_size 2
#evaluate_size 4
#evaluate_size 8
evaluate_size 16
#evaluate_size 32
#evaluate_size 64
#evaluate_size 128
#evaluate_size 256
#evaluate_size 512
#evaluate_size 1024
echo "Performance test finished"