"""Score raw outputs: task score (lenient parsing) + strict format compliance, per item.

Usage: python src/score.py  -> results/scored.csv (all results/raw/*.jsonl except pilots)
"""
import glob, json, os, re, string
from collections import Counter

import pandas as pd
from rouge_score import rouge_scorer

ROOT = os.path.join(os.path.dirname(__file__), "..")
LABELS = ["World", "Sports", "Business", "Sci/Tech"]
_rouge = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)


def load_items():
    items = {}
    for t in ["cls", "ext", "gen", "rsn"]:
        with open(os.path.join(ROOT, "datasets", f"{t}.jsonl")) as f:
            for l in f:
                r = json.loads(l)
                items[(t, r["id"])] = r
    return items


# ---------------- classification ----------------
def cls_pred(out):
    """Lenient: earliest-mentioned label (with common synonyms)."""
    syn = {"World": ["world", "politics"], "Sports": ["sports", "sport"],
           "Business": ["business", "economy", "finance"],
           "Sci/Tech": ["sci/tech", "science", "technology", "sci-tech", "scitech", "tech"]}
    low = out.lower()
    best, pos = None, 10**9
    for lab, ws in syn.items():
        for w in ws:
            m = re.search(r"\b" + re.escape(w) + r"\b", low)
            if m and m.start() < pos:
                best, pos = lab, m.start()
    return best


def cls_compliant(out):
    return out.strip() in LABELS


# ---------------- extraction (SQuAD official normalisation) ----------------
def _norm(s):
    s = s.lower()
    s = "".join(ch for ch in s if ch not in set(string.punctuation))
    s = re.sub(r"\b(a|an|the)\b", " ", s)
    return " ".join(s.split())


def _f1(pred, gold):
    p, g = _norm(pred).split(), _norm(gold).split()
    common = Counter(p) & Counter(g)
    ns = sum(common.values())
    if ns == 0:
        return 0.0
    pr, rc = ns / len(p), ns / len(g)
    return 2 * pr * rc / (pr + rc)


def ext_clean(out):
    """Lenient: first non-empty line, strip 'Answer:' prefixes and quotes."""
    lines = [l for l in out.strip().splitlines() if l.strip()]
    s = lines[0] if lines else ""
    s = re.sub(r"^(answer|answer span)\s*:\s*", "", s.strip(), flags=re.I)
    return s.strip().strip('"\'“”')


def ext_compliant(out, context):
    s = out.strip()
    if not s or "\n" in s:
        return False
    s2 = s.rstrip(".")
    return (s in context or s2 in context) and len(s.split()) <= 30


# ---------------- generation ----------------
def sentences(text):
    return [x for x in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'“])", text.strip()) if x.strip()]


def gen_clean(out):
    s = out.strip()
    s = re.sub(r"^(summary|here is (a|the) summary[^:]*)\s*:\s*", "", s, flags=re.I)
    return s


def gen_compliant(out):
    s = out.strip()
    if not s:
        return False
    if re.search(r"^\s*([-*•#]|\d+\.)\s", s, flags=re.M) or "**" in s:
        return False
    if re.match(r"^(summary|here is|here's|this article|the article)", s, flags=re.I):
        return False
    if "\n\n" in s:
        return False
    return 2 <= len(sentences(s)) <= 4 and len(s.split()) <= 80


# ---------------- reasoning ----------------
_num = r"-?\$?\d[\d,]*(?:\.\d+)?"


def _to_float(x):
    try:
        return float(x.replace(",", "").replace("$", "").rstrip("."))
    except ValueError:
        return None


def rsn_pred(out):
    m = re.findall(r"final answer\s*[:：]?\s*\**\s*(" + _num + ")", out, flags=re.I)
    if m:
        return _to_float(m[-1])
    nums = re.findall(_num, out)
    return _to_float(nums[-1]) if nums else None


def rsn_compliant(out):
    lines = [l.strip() for l in out.strip().splitlines() if l.strip()]
    return bool(lines) and re.fullmatch(r"Final answer: -?\d+(\.\d+)?", lines[-1]) is not None


def score_row(r, item):
    t, out = r["task"], r["output"]
    d = {}
    if t == "cls":
        d["score"] = float(cls_pred(out) == item["label"])
        d["compliant"] = cls_compliant(out)
    elif t == "ext":
        p = ext_clean(out)
        d["em"] = float(max(_norm(p) == _norm(g) for g in item["answers"]))
        d["score"] = max(_f1(p, g) for g in item["answers"])  # token F1 is the primary metric
        d["compliant"] = ext_compliant(out, item["context"])
    elif t == "gen":
        sc = _rouge.score(item["reference"], gen_clean(out))
        d["score"] = sc["rougeL"].fmeasure
        d["rouge1"], d["rouge2"] = sc["rouge1"].fmeasure, sc["rouge2"].fmeasure
        d["n_words"] = len(out.split())
        d["compliant"] = gen_compliant(out)
    elif t == "rsn":
        p = rsn_pred(out)
        d["score"] = float(p is not None and abs(p - float(item["answer"])) < 1e-6)
        d["compliant"] = rsn_compliant(out)
    return d


def main():
    items = load_items()
    rows = []
    for fn in sorted(glob.glob(os.path.join(ROOT, "results", "raw", "*.jsonl"))):
        if "_pilot" in fn:
            continue
        tag = os.path.basename(fn)[:-6]
        with open(fn) as f:
            for l in f:
                r = json.loads(l)
                d = score_row(r, items[(r["task"], r["id"])])
                rows.append({"model": tag, "task": r["task"], "condition": r["condition"], "id": r["id"],
                             "prompt_tokens": r["prompt_tokens"], "output_tokens": r["output_tokens"],
                             "truncated": r["finish_reason"] == "length", **d})
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(ROOT, "results", "scored.csv"), index=False)
    print(df.groupby(["model", "task", "condition"])[["score", "compliant"]].mean().unstack().round(3))


if __name__ == "__main__":
    main()
