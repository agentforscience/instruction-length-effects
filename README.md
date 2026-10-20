# Instruction Length and Task Performance: When More Detail Hurts

Tests whether longer, more detailed task instructions help or hurt LLMs. We used 5 nested tiers (minimal ~18 words → exhaustive ~900 words) plus a length-matched padded control. The tasks span classification (AG News), extraction (SQuAD), generation (CNN/DM) and reasoning (GSM8K), on Qwen2.5-Instruct 0.5B/1.5B/3B/7B/14B run locally with vLLM (252 paired items per cell, 30k+ generations in total).

## Key findings
- **3B–14B models: length barely matters.** Standard → exhaustive changes are within ±1.6 pts on every task. The predicted 3–7% exhaustive penalty for classification and extraction did not appear (H1 not supported).
- **Harm is a tiny-model effect.** 0.5B classification falls from 62% (minimal) to 39% (exhaustive) as predictions collapse onto one label. The standard→exhaustive drop shrinks with size (ρ = −0.9), but **7B ≈ 14B** (H4 as stated not supported).
- **Not attention dilution.** ~700 words of irrelevant filler never hurt any model, and for small models it *helped* relative to standard. Damage comes from instruction content and its position right before the input. System-message placement reduces it.
- **Generation** improves slightly and monotonically with detail for ≥3B (+0.3–0.6 ROUGE-L per tier). **Reasoning** shows no significant differences beyond concise (H3 largely supported). **Compliance** saturates from *concise* for ≥7B and does not peak at standard (H5 not supported).
- Biggest single lever: minimal → concise for extraction (+10 F1 at 7B/14B, by fixing over-long spans).

Full details: [REPORT.md](REPORT.md). Plan: [planning.md](planning.md).

## Reproduce
```bash
uv venv --python 3.12 && source .venv/bin/activate && uv sync
N_ITEMS=252 python src/data.py          # samples from local HF cache -> datasets/
GPU=0 ./run_all.sh                       # vLLM runs -> results/raw/
python src/score.py && python src/analyze.py && python src/diagnostics.py && python src/placement.py
```
Needs a GPU with ~16 GB (7B) or ~40 GB (14B bf16). HF cache path: `HF_HOME=/data/transformers`.

## Layout
- `src/prompts.py`: all instruction tiers + padding filler (full prompt text)
- `src/data.py`, `src/run_model.py`, `src/score.py`, `src/analyze.py`, `src/diagnostics.py`, `src/placement.py`
- `datasets/*.jsonl`: evaluation items
- `results/raw/`: every generation · `results/scored.csv`: item-level scores · `results/summary_table.csv`, `tests.csv`, `hypotheses.json`, `diagnostics.csv`, `placement.csv`, `error_examples.md`
- `figures/`: score_by_tier, compliance_by_tier, drop_by_model
- `logs/`: run logs and status
