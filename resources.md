# Resources used

The resource-finder stage was skipped for this workspace (no papers/, code/ or pre-downloaded datasets were provided). Everything was taken from the host's local HuggingFace cache (`/data/transformers/hub`):

- Datasets: fancyzhx/ag_news (test), rajpurkar/squad (validation), abisee/cnn_dailymail 3.0.0 (test), openai/gsm8k (test). Samples are in `datasets/*.jsonl` (built by `src/data.py`, seed 42, n = 252 each).
- Models: Qwen/Qwen2.5-{0.5B,1.5B,3B,7B,14B}-Instruct (bf16). Downloaded but not run because of GPU contention: Qwen/Qwen2.5-32B-Instruct-AWQ, Qwen/Qwen2.5-14B-Instruct-AWQ. Planned but not run: hugging-quants/Meta-Llama-3.1-8B-Instruct-AWQ-INT4.
- No API keys were available, so all LLM outputs come from local vLLM inference.
- Literature context (from background knowledge, cited in REPORT.md): Shi et al. 2023; Liu et al. 2023; Levy et al. 2024; IFEval; FollowBench.
