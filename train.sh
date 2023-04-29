python ./run_summarization.py \
    --model_name_or_path t5-small \
    --do_train True\
    --do_predict True\
    --train_file ./data/train.csv \
    --test_file ./data/test.csv \
    --source_prefix "Generate a description of the following university course based on its title: " \
    --max_source_length 128 \
    --max_target_length 2048 \
    --output_dir ./output3 \
    --overwrite_output_dir True \
    --per_device_train_batch_size=2 \
    --per_device_eval_batch_size=4 \
    --predict_with_generate True\
    --save_steps 5000 \
    --run_name final582