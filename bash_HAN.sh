DATA=("IA_F" "IB_F" "IIA_F" "IIB_F" "IA_F_BPE" "IB_F_BPE" "IIA_F_BPE" "IIB_F_BPE")
MAX_NUM_WORDS=("500" "20000")
DIM_LSTM=("100" "500")
OPTIMIZER=("adam" "rmsprop")

for i in ${DATA[@]}; do
    for j in ${MAX_NUM_WORDS[@]}; do
        for k in ${DIM_LSTM[@]}; do
                for o in ${OPTIMIZER[@]}; do

                    python3 RunHAN.py --data ${i} --labels labels --max_num_words ${j} --dim_LSTM ${k} --optimizer ${o}

                done
            done
        done
    done
done