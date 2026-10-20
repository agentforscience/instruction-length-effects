#!/bin/bash
# Wait for any GPU with enough free memory, then launch; for the leftover models.
cd "$(dirname "$0")"
export HF_HOME=/data/transformers HF_HUB_OFFLINE=1 VLLM_USE_FLASHINFER_SAMPLER=0
go() { # model tag memGB
  while [ ! -s results/raw/$2.jsonl ]; do
    g=$(nvidia-smi --query-gpu=index,memory.free --format=csv,noheader,nounits | awk -v n=$(( ($3+1)*1024 )) -F', ' '$2>n{print $1; exit}')
    if [ -n "$g" ]; then
      CUDA_VISIBLE_DEVICES=$g .venv/bin/python src/run_model.py --model $1 --tag $2 --gpu-mem-gb $3 > logs/run_$2.log 2>&1 && echo "$2 ok (gpu$g)" >> logs/status.txt || echo "$2 fail gpu$g" >> logs/status.txt
    fi
    sleep 30
  done
}
go hugging-quants/Meta-Llama-3.1-8B-Instruct-AWQ-INT4 llama3.1-8b-awq 10
go Qwen/Qwen2.5-32B-Instruct-AWQ qwen2.5-32b-awq 26
echo WAITDONE >> logs/status.txt
