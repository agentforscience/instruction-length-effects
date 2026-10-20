# Planning: Instruction Length and Task Performance — When More Detail Hurts

## Motivation & Novelty Assessment

### Why This Research Matters
Practitioners routinely write very long system prompts / task instructions ("prompt bloat"), on the
intuition that more detail cannot hurt. If instruction length has a task-dependent optimum, that
directly affects how prompts should be written, especially for small open models deployed on-device
or at low cost, where the effect may be largest.

### Gap in Existing Work
The resource-finder stage was skipped for this workspace (no `papers/`, `datasets/`, `code/`), so this
is based on background knowledge of the literature. Prior work shows (a) LLM accuracy drops as
*input context* grows even when the extra text is irrelevant (Levy et al. 2024 "Same Task, More
Tokens"; Shi et al. 2023 "LLMs can be easily distracted by irrelevant context"; Liu et al. 2023
"Lost in the Middle"), and (b) instruction-following degrades as the *number of constraints* grows
(e.g. IFEval / FollowBench / "How many instructions can LLMs follow at once"). Few studies vary the
**length/detail of the task instruction itself** in graded tiers, across **task types**
(classification, extraction, generation, reasoning) and **model scales**, and few separate the
effect of *more content* from *more tokens*.

### Our Novel Contribution
1. A controlled 5-tier, nested instruction ladder (minimal → concise → standard → detailed →
   exhaustive) applied to four task types with the same core output-format constraint in every tier.
2. A **length-matched padding control** (standard content + task-irrelevant filler padded to the
   exhaustive length) that separates "attention dilution by tokens" from "effect of extra content".
3. A within-family scale sweep (Qwen2.5 3B/7B/14B, + Llama-3.1-8B as a second family) to test the
   claim that small models are hurt more by exhaustive instructions.
4. Format-compliance measured separately from task correctness.

### Experiment Justification
- Exp 1 (tier sweep × 4 tasks × models): directly tests the main per-task predictions
  (peak at standard for classification/extraction; monotonic for generation; flat for reasoning).
- Exp 2 (padding control): if exhaustive hurts, is it the tokens (dilution) or the content
  (over-specification, conflicting/extra rules)? Without it, "attention dilution" is unfalsifiable.
- Exp 3 (scale comparison): tests "7B degrades more than larger models".
- Exp 4 (compliance analysis): tests "compliance peaks at standard across all tasks".

## Research Question
How does the length/detail of a task instruction (5 graded tiers) affect accuracy and output-format
compliance of instruction-tuned LLMs, and does this depend on task type and model size?

## Hypothesis Decomposition
- H1 (classification, extraction): score(standard) > score(exhaustive) by 3–7 points; standard is the
  argmax tier.
- H2 (generation): score increases monotonically minimal → detailed (exhaustive unspecified).
- H3 (reasoning): no significant difference among concise, standard, detailed, exhaustive.
- H4 (scale): drop(standard→exhaustive) is larger for 7B than for 14B.
- H5 (compliance): compliance argmax is the standard tier for every task.
- Auxiliary H6: padded-standard ≈ exhaustive would support a pure length/dilution account;
  padded-standard ≈ standard would indicate content, not length, drives any change.

## Proposed Methodology

### Approach
No API keys are available on this host (OPENROUTER_KEY unset), so we run real open-weight
instruction-tuned models locally with vLLM (greedy decoding). This is well suited to the hypothesis,
which is explicitly about 7B vs larger models.

Models: Qwen2.5-3B-Instruct, Qwen2.5-7B-Instruct, Qwen2.5-14B-Instruct (same family, scale sweep),
Llama-3.1-8B-Instruct (AWQ-INT4; second family). Optional: Qwen2.5-32B-Instruct-AWQ if GPU allows.

Tasks / datasets (local HF cache):
| Type | Dataset | Metric | Core format constraint (in every tier) |
|---|---|---|---|
| Classification | AG News test (4-way topic) | accuracy | answer only one label word |
| Extraction | SQuAD v1.1 validation | EM / token F1 | answer is an exact span copied from passage, nothing else |
| Generation | CNN/DailyMail 3.0.0 test | ROUGE-L / ROUGE-1/2 vs highlights | 2–4 sentences, ≤ 80 words, plain text |
| Reasoning | GSM8K test | accuracy | end with `Final answer: <number>` |

n = 250 items per task (fixed seed 42 sample), identical across conditions.

Tiers (nested: each tier contains the previous tier's content plus more):
- minimal (~10–20 words): task + format constraint only.
- concise (~40–60 words): + label/definition basics.
- standard (~120–180 words): + clear definitions, key decision rules.
- detailed (~350–450 words): + edge cases, tie-breaking, worked guidance, quality criteria.
- exhaustive (~1,000–1,300 words): + extensive elaboration, many additional rules, redundancy,
  rationale, rare edge cases (the "kitchen-sink" prompt practitioners write).
- padded control: standard text + task-irrelevant neutral filler (generic text about the
  organization's documentation policies) to match exhaustive token length.

### Baselines
The minimal tier is the baseline; the padded control is the length-matched baseline for exhaustive.
Majority-class / random baselines are reported for classification.

### Evaluation Metrics
Task score (accuracy, EM/F1, ROUGE-L, accuracy) computed with lenient parsing so correctness is
not confounded by format; compliance (strict adherence to the core format constraint) reported
separately.

### Statistical Analysis Plan
- Per model×task: paired bootstrap (10k resamples over items) CIs for each tier and for differences
  (standard − exhaustive, etc.). Paired tests: McNemar (binary metrics) / Wilcoxon signed-rank
  (continuous). Holm correction within each family of comparisons. α = 0.05.
- Trend for generation: Page's / Spearman trend of item-level scores vs tier index; also check
  pairwise monotonicity.
- Scale: difference-in-differences of (standard − exhaustive) between 7B and 14B with bootstrap CI.

## Expected Outcomes
Support: classification/extraction curves inverted-U with peak at standard and 3–7pt drop at
exhaustive; generation increases to detailed; GSM8K flat beyond concise; 7B drop > 14B drop.
Refute: flat or monotone curves for classification/extraction; no scale interaction; compliance
peaks elsewhere.

## Timeline and Milestones
Setup + prompts (1h) → pilot 20 items (15 min) → full runs (~1–2h GPU, shared) → analysis (45 min)
→ report (30 min).

## Potential Challenges
- Shared GPUs with fluctuating free memory → small `gpu_memory_utilization`, AWQ models, retry loop.
- Single prompt wording per tier confounds wording with length → nested design, padding control;
  acknowledge as limitation.
- ROUGE is a weak generation metric → also report length/compliance; acknowledge.

## Success Criteria
All 6 conditions × 4 tasks run for ≥3 models; statistical tests computed; each sub-hypothesis
explicitly judged supported / not supported in REPORT.md.
