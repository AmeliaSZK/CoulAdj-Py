#!/usr/bin/env bash

# TEST PARAMETERS
CLI_FLAGS=''

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
    #echo "~ Size $1 ~ "
    $COMMAND "$SAMPLE" "$RESULT"
    cmp --silent "$GOLDEN" "$RESULT" || echo "Size $1 failed"
}

echo "~~~ Testing correctness at sizes 1 and 8 ~~~"
evaluate_size 1
#evaluate_size 2
evaluate_size 8
echo "~~~ Correctness test finished ~~~"
echo "If no failure was reported, then all were correct."
