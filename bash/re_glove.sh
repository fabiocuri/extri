#!/bin/bash
set -e

# Makes programs, downloads sample data, trains a GloVe model, and then evaluates it.
# One optional argument can specify the language used for eval script: matlab, octave or [default] python

make

DATA=("re_train_original" "re_train_original_BPE" "re_train_preprocessed" "re_train_preprocessed_BPE")

for NAME in ${DATA[@]}; do

    CORPUS=${NAME}.txt
    VOCAB_FILE=vocab_${NAME}.txt
    COOCCURRENCE_FILE=cooccurrence_${NAME}.bin
    COOCCURRENCE_SHUF_FILE=cooccurrence_${NAME}.shuf.bin
    BUILDDIR=build
    SAVE_FILE=vectors_${NAME}
    VERBOSE=2
    MEMORY=4.0
    VOCAB_MIN_COUNT=5
    VECTOR_SIZE=100
    MAX_ITER=15
    WINDOW_SIZE=15
    BINARY=2
    NUM_THREADS=8
    X_MAX=10

    echo
    echo "$ $BUILDDIR/vocab_count -min-count $VOCAB_MIN_COUNT -verbose $VERBOSE < $CORPUS > $VOCAB_FILE"
    $BUILDDIR/vocab_count -min-count $VOCAB_MIN_COUNT -verbose $VERBOSE < $CORPUS > $VOCAB_FILE
    echo "$ $BUILDDIR/cooccur -memory $MEMORY -vocab-file $VOCAB_FILE -verbose $VERBOSE -window-size $WINDOW_SIZE < $CORPUS > $COOCCURRENCE_FILE"
    $BUILDDIR/cooccur -memory $MEMORY -vocab-file $VOCAB_FILE -verbose $VERBOSE -window-size $WINDOW_SIZE < $CORPUS > $COOCCURRENCE_FILE
    echo "$ $BUILDDIR/shuffle -memory $MEMORY -verbose $VERBOSE < $COOCCURRENCE_FILE > $COOCCURRENCE_SHUF_FILE"
    $BUILDDIR/shuffle -memory $MEMORY -verbose $VERBOSE < $COOCCURRENCE_FILE > $COOCCURRENCE_SHUF_FILE
    echo "$ $BUILDDIR/glove -save-file $SAVE_FILE -threads $NUM_THREADS -input-file $COOCCURRENCE_SHUF_FILE -x-max $X_MAX -iter $MAX_ITER -vector-size $VECTOR_SIZE -binary $BINARY -vocab-file $VOCAB_FILE -verbose $VERBOSE"
    $BUILDDIR/glove -save-file $SAVE_FILE -threads $NUM_THREADS -input-file $COOCCURRENCE_SHUF_FILE -x-max $X_MAX -iter $MAX_ITER -vector-size $VECTOR_SIZE -binary $BINARY -vocab-file $VOCAB_FILE -verbose $VERBOSE
    if [ "$CORPUS" = 'text8' ]; then
       if [ "$1" = 'matlab' ]; then
           matlab -nodisplay -nodesktop -nojvm -nosplash < ./eval/matlab/read_and_evaluate.m 1>&2 
       elif [ "$1" = 'octave' ]; then
           octave < ./eval/octave/read_and_evaluate_octave.m 1>&2
       else
           echo "$ python eval/python/evaluate.py"
           python eval/python/evaluate.py
       fi
    fi
done
