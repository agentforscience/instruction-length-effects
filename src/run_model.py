"""Run one model on all tasks x conditions with vLLM (greedy decoding) and save raw outputs.

Usage: python src/run_model.py --model <hf_id> --tag <short_name> [--gpu-mem-gb 14] [--limit N]
Output: results/raw/<tag>.jsonl  (one line per (task, condition, item))
"""
import argparse, json, os, sys, time

sys.path.insert(0, os.path.dirname(__file__))
from prompts import CONDITIONS, build_instruction  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
MAX_TOKENS = {"cls": 16, "ext": 64, "gen": 200, "rsn": 768}


def format_input(task, item):
    """Task input appended after the instruction (identical across conditions)."""
    if task == "cls":
        return f"Article: {item['input']}\n\nCategory:"
    if task == "ext":
        return f"Passage: {item['context']}\n\nQuestion: {item['question']}\n\nAnswer:"
    if task == "gen":
        return f"Article: {item['input']}\n\nSummary:"
    if task == "rsn":
        return f"Problem: {item['input']}"
    raise ValueError(task)


def load(task, limit=None):
    with open(os.path.join(ROOT, "datasets", f"{task}.jsonl")) as f:
        rows = [json.loads(l) for l in f]
    return rows[:limit] if limit else rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--gpu-mem-gb", type=float, default=14.0)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--max-model-len", type=int, default=4096)
    ap.add_argument("--system", action="store_true",
                    help="robustness variant: instruction in the system message, task input in the user turn")
    args = ap.parse_args()

    import torch
    from vllm import LLM, SamplingParams

    total = torch.cuda.get_device_properties(0).total_memory / 2**30
    llm = LLM(model=args.model, gpu_memory_utilization=min(0.95, args.gpu_mem_gb / total),
              max_model_len=args.max_model_len, max_num_seqs=64, seed=42, enforce_eager=False)

    meta, convs, sps = [], [], []
    for task in MAX_TOKENS:
        for cond in CONDITIONS:
            instr = build_instruction(task, cond)
            for item in load(task, args.limit):
                if args.system:
                    convs.append([{"role": "system", "content": instr},
                                  {"role": "user", "content": format_input(task, item)}])
                else:
                    convs.append([{"role": "user", "content": instr + "\n\n" + format_input(task, item)}])
                sps.append(SamplingParams(temperature=0.0, max_tokens=MAX_TOKENS[task], seed=42))
                meta.append({"task": task, "condition": cond, "id": item["id"]})
    print(f"{len(convs)} requests", flush=True)
    t0 = time.time()
    outs = llm.chat(convs, sps, use_tqdm=True)
    dt = time.time() - t0
    out_path = os.path.join(ROOT, "results", "raw", f"{args.tag}{'_pilot' if args.limit else ''}.jsonl")
    with open(out_path, "w") as f:
        for m, o in zip(meta, outs):
            m.update(model=args.model, output=o.outputs[0].text,
                     prompt_tokens=len(o.prompt_token_ids), output_tokens=len(o.outputs[0].token_ids),
                     finish_reason=o.outputs[0].finish_reason)
            f.write(json.dumps(m) + "\n")
    print(f"saved {out_path} in {dt:.0f}s", flush=True)


if __name__ == "__main__":
    main()
