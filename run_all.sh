#!/bin/bash
# Sequentially run all models on one GPU; skip finished ones; retry on startup failure.
cd "$(dirname "$0")"
export HF_HOME=/data/transformers HF_HUB_OFFLINE=1 VLLM_USE_FLASHINFER_SAMPLER=0 CUDA_VISIBLE_DEVICES=${GPU:-2}
run() { # model tag memGB
  [ -s results/raw/$2.jsonl ] && { echo "skip $2"; return; }
  for a in 1 2 3 4 5; do
    .venv/bin/python src/run_model.py --model $1 --tag $2 --gpu-mem-gb $3 > logs/run_$2.log 2>&1 && { echo "$2 ok" >> logs/status.txt; return; }
    echo "$2 fail attempt $a" >> logs/status.txt; sleep 60
  done
}
run Qwen/Qwen2.5-7B-Instruct qwen2.5-7b 30
run Qwen/Qwen2.5-14B-Instruct qwen2.5-14b 42
run Qwen/Qwen2.5-3B-Instruct qwen2.5-3b 24
run Qwen/Qwen2.5-1.5B-Instruct qwen2.5-1.5b 20
run hugging-quants/Meta-Llama-3.1-8B-Instruct-AWQ-INT4 llama3.1-8b-awq 24
[ -n "$(ls /data/transformers/hub/models--Qwen--Qwen2.5-32B-Instruct-AWQ/snapshots/*/model-00005-of-00005.safetensors 2>/dev/null)" ] && run Qwen/Qwen2.5-32B-Instruct-AWQ qwen2.5-32b-awq 42
echo ALLDONE >> logs/status.txt
