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

echo "~~~ Profiling Sizes 1 to 512 ~~~"
echo "Each size should take ~4x longer than the previous."
evaluate_size 1
evaluate_size 2
evaluate_size 4
evaluate_size 8
evaluate_size 16
evaluate_size 32
evaluate_size 64
evaluate_size 128
evaluate_size 256
evaluate_size 512
#evaluate_size 1024
echo "~~~ Profiling of all sizes finished ~~~"
echo "Truncate durations to 4 digits before calculating & recording ratios."
echo "  \"Truncate to 4 digits\" will give you 5 chars bc of the decimal point."
echo "  \"Recording ratios\" means to write them in all_sizes.tsv"
