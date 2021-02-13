#!/usr/bin/env bash

# TEST PARAMETERS
CLI_FLAGS='--profile'

# PROJECT PARAMETERS
PROGRAM='python ./CoulAdj-Py.py'
SAMPLES_DIR='./tests/samples/'
RESULTS_DIR='./tests/results/'
GOLDEN_DIR='./tests/'
# (Make sure the DIR variables end with a /backslash/ )

# ~~~ END OF PARAMETERS ~~~


GOLDEN="${GOLDEN_DIR}golden.tsv"
COMMAND="${PROGRAM} ${CLI_FLAGS}"

evaluate_size(){
    local SAMPLE="${SAMPLES_DIR}sample-size-$1.png"
    local RESULT="${RESULTS_DIR}result-size-$1.tsv"
    echo -n "Size $1: "
    $COMMAND "$SAMPLE" "$RESULT"
    cmp --silent "$GOLDEN" "$RESULT" || echo "Size $1 failed"
}

echo "~~~ Profiling Sizes 8 to 64 ~~~"
echo "Expect 6~12 seconds to do size 64"
#evaluate_size 1
#evaluate_size 2
#evaluate_size 4
evaluate_size 8
evaluate_size 16
evaluate_size 32
evaluate_size 64
#evaluate_size 128
#evaluate_size 256
#evaluate_size 512
#evaluate_size 1024
echo "~~~ Temporal complexity test finished ~~~"
echo "At O(n), each size takes ~4x longer than the previous."
echo "Actual ratios have ranged from 3.4x to 4.2x"
