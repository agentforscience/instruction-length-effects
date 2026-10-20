#!/bin/bash
cd "$(dirname "$0")"
export HF_HOME=/data/transformers HF_HUB_OFFLINE=1 VLLM_USE_FLASHINFER_SAMPLER=0 CUDA_VISIBLE_DEVICES=3
.venv/bin/python src/run_model.py --model Qwen/Qwen2.5-0.5B-Instruct --tag qwen2.5-0.5b --gpu-mem-gb 5 > logs/run_qwen2.5-0.5b.log 2>&1 && echo "qwen2.5-0.5b ok (gpu3)" >> logs/status.txt
.venv/bin/python src/run_model.py --model Qwen/Qwen2.5-1.5B-Instruct --tag sys_qwen2.5-1.5b --system --gpu-mem-gb 5.3 > logs/run_sys_qwen2.5-1.5b.log 2>&1 && echo "sys_qwen2.5-1.5b ok (gpu3)" >> logs/status.txt
