set -eux

export CUDA_VISIBLE_DEVICES=0 
export BATCH_SIZE=32
export CKPT=./checkpoints/model_50040.pdparams
export DATASET_FILE=./data/test_data.json

python run_duie.py \
    --do_predict \
    --init_checkpoint $CKPT \
    --predict_data_file $DATASET_FILE \
    --max_seq_length 512 \
    --batch_size $BATCH_SIZE

